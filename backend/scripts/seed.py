from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import async_session_maker
from app.models import Category, Product, Supplier, Unit, User
from app.models.enums import (
    ProductStatus,
    SupplierStatus,
    UserRole,
    UserStatus,
)
import json
from datetime import date, datetime
from decimal import Decimal
from typing import Any, cast

DATA_DIR = BACKEND_ROOT / "data" / "clean"
JSON_CATEGORIES = DATA_DIR / "categories_seed.json"
JSON_SUPPLIERS = DATA_DIR / "suppliers_seed.json"
JSON_UNITS = DATA_DIR / "units_seed.json"
JSON_PRODUCTS = DATA_DIR / "products_seed.json"

def _parse_date(raw: Any) -> date | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None

def _parse_decimal(raw: Any, default: Decimal | None = None) -> Decimal | None:
    if raw is None:
        return default
    s = str(raw).strip()
    if not s:
        return default
    try:
        return Decimal(s)
    except Exception:
        return default


def _load_json_list(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        print(f"[seed] JSON not found, skip: {path}")
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Invalid JSON format (expected list): {path}")
    return [x for x in data if isinstance(x, dict)]


#  ========================================
#  1. CREATE USERS
#  ========================================

SEED_PASSWORD = "changeme123"
SEED_USERS: list[dict] = [
    {"user_name": "Demo Manager", "role": UserRole.manager, "email": "manager@demo.smartstock"},
    {"user_name": "Demo Staff", "role": UserRole.staff, "email": "staff@demo.smartstock"},
]

def _hash_password(password: str) -> str:
    """
    Try bcrypt first (matches historical config), but fallback to pbkdf2_sha256
    if the container's bcrypt dependency is incompatible.
    """
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    except Exception as e:
        print(f"bcrypt hashing failed; fallback to pbkdf2_sha256: {e}")
        return pbkdf2_sha256.hash(password)

async def seed_users(*, force: bool) -> None:
    password_hash = _hash_password(SEED_PASSWORD)

    print("Seeding users (idempotent)...")
    async with async_session_maker() as session:
        for u in SEED_USERS:
            stmt = select(User).where(User.email == u["email"])
            result = await session.execute(stmt)
            existing: User | None = result.scalar_one_or_none()

            if existing is None:
                session.add(
                    User(
                        user_name=u["user_name"],
                        hash_password=password_hash,
                        role=u["role"],
                        email=u["email"],
                        status=UserStatus.active,
                    )
                )
                print(f"  - added {u['email']}")
            elif force:
                existing.user_name = u["user_name"]
                existing.hash_password = password_hash
                existing.role = u["role"]
                existing.status = UserStatus.active
                session.add(existing)
                print(f"  - updated {u['email']} (force)")
            else:
                print(f"  - exists {u['email']} (skip)")

        await session.commit()

#  ========================================
#  2. CREATE SUPPLIERS
#  ========================================

def _parse_supplier_status(raw: Any) -> SupplierStatus:
    s = str(raw).strip() if raw is not None else ""
    if not s:
        return SupplierStatus.active
    try:
        return SupplierStatus(s)
    except ValueError:
        return SupplierStatus.active

async def seed_suppliers_from_json(session, *, force: bool) -> None:
    suppliers_data = _load_json_list(JSON_SUPPLIERS)
    if not suppliers_data:
        return

    names = [s.get("supplier_name") for s in suppliers_data if s.get("supplier_name")]
    if not names:
        return

    existing_result = await session.execute(
        select(Supplier).where(cast(Any, Supplier.supplier_name).in_(names))
    )
    existing_by_name = {s.supplier_name: s for s in existing_result.scalars().all()}

    for s in suppliers_data:
        name = s.get("supplier_name")
        if not name:
            continue
        status = _parse_supplier_status(s.get("status"))
        if name not in existing_by_name:
            session.add(Supplier(supplier_name=name, status=status))
        elif force:
            existing_by_name[name].status = status
            session.add(existing_by_name[name])

    await session.commit()

#  ========================================
#  3. CREATE CATEGORIES
#  ========================================

async def seed_categories_from_json(session, *, force: bool) -> dict[str, Any]:
    categories_data = _load_json_list(JSON_CATEGORIES)
    if not categories_data:
        return {}

    names = [c.get("category_name") for c in categories_data if c.get("category_name")]
    if not names:
        return {}

    existing_result = await session.execute(
        select(Category).where(cast(Any, Category.category_name).in_(names))
    )
    existing_by_name = {c.category_name: c for c in existing_result.scalars().all()}

    for c in categories_data:
        name = c.get("category_name")
        if not name:
            continue
        if name not in existing_by_name:
            session.add(Category(category_name=name, description=c.get("description")))
        elif force:
            existing = existing_by_name[name]
            if "description" in c:
                existing.description = c.get("description")
            session.add(existing)

    await session.commit()

    after = await session.execute(
        select(cast(Any, Category.id), cast(Any, Category.category_name)).where(
            cast(Any, Category.category_name).in_(names)
        )
    )
    return {row.category_name: row.id for row in after.all()}

#  ========================================
#  4. CREATE UNITS
#  ========================================

def _units_seed_rows() -> list[dict[str, Any]]:
    return _load_json_list(JSON_UNITS)


def _first_seeded_unit_id(unit_id_by_name: dict[str, Any]) -> Any | None:
    for row in _units_seed_rows():
        name = str(row.get("unit_name") or "").strip()
        if name and name in unit_id_by_name:
            return unit_id_by_name[name]
    return None


async def seed_units_from_json(session, *, force: bool) -> dict[str, Any]:
    units_data = _units_seed_rows()
    names = [str(u["unit_name"]).strip() for u in units_data if u.get("unit_name")]
    names = [n for n in names if n]
    if not names:
        return {}

    existing_result = await session.execute(select(Unit).where(cast(Any, Unit.unit_name).in_(names)))
    existing_by_name = {x.unit_name: x for x in existing_result.scalars().all()}

    for u in units_data:
        name = str(u.get("unit_name") or "").strip()
        if not name:
            continue
        symbol_raw = u.get("unit_symbol")
        symbol = str(symbol_raw).strip() if symbol_raw is not None else None
        if symbol == "":
            symbol = None
        if name not in existing_by_name:
            session.add(Unit(unit_name=name, unit_symbol=symbol))
        elif force:
            existing_by_name[name].unit_symbol = symbol
            session.add(existing_by_name[name])

    await session.commit()

    after = await session.execute(
        select(cast(Any, Unit.id), cast(Any, Unit.unit_name)).where(cast(Any, Unit.unit_name).in_(names))
    )
    return {row.unit_name: row.id for row in after.all()}

#  ========================================
#  5. CREATE PRODUCTS
#  ========================================

def _parse_product_status(raw: Any) -> ProductStatus:
    s = str(raw).strip() if raw is not None else ""
    if not s:
        return ProductStatus.in_stock
    try:
        return ProductStatus(s)
    except ValueError:
        return ProductStatus.in_stock


async def seed_products_from_json(
    session,
    *,
    force: bool,
    category_id_by_name: dict[str, Any],
    base_unit_id: Any,
    limit_products: int | None = None,
    batch_size: int = 200,
) -> None:
    products_data = _load_json_list(JSON_PRODUCTS)
    if not products_data:
        return

    if limit_products is not None:
        products_data = products_data[: max(0, limit_products)]

    sku_codes = [p.get("sku_code") for p in products_data if p.get("sku_code")]
    existing_by_sku: dict[str, Product] = {}
    if sku_codes:
        existing_result = await session.execute(
            select(Product).where(cast(Any, Product.sku_code).in_(sku_codes))
        )
        existing_by_sku = {p.sku_code: p for p in existing_result.scalars().all()}

    pending = 0
    for p in products_data:
        sku = p.get("sku_code")
        if not sku:
            continue

        category_name = p.get("category_name")
        category_id = category_id_by_name.get(category_name) if category_name else None
        if category_id is None:
            continue

        status = _parse_product_status(p.get("status"))
        expiry = _parse_date(p.get("expiry_date"))

        stock_quantity = _parse_decimal(p.get("stock_quantity"), default=Decimal("0")) or Decimal("0")
        sales_volume = _parse_decimal(p.get("sales_volume"), default=Decimal("0")) or Decimal("0")
        reorder_level = _parse_decimal(p.get("reorder_level"))
        last_unit_price = _parse_decimal(p.get("last_unit_price"))

        if sku in existing_by_sku:
            if not force:
                continue
            prod = existing_by_sku[sku]
            prod.category_id = category_id
            prod.base_unit_id = base_unit_id
            prod.product_name = p.get("product_name") or sku
            prod.sku_code = sku
            prod.warehouse_location = p.get("warehouse_location")
            prod.stock_quantity = stock_quantity
            prod.sales_volume = sales_volume
            prod.reorder_level = reorder_level
            prod.last_unit_price = last_unit_price
            prod.currency = p.get("currency") or "AUD"
            prod.status = status
            prod.expiry_date = expiry
            session.add(prod)
        else:
            session.add(
                Product(
                    category_id=category_id,
                    base_unit_id=base_unit_id,
                    sku_code=sku,
                    product_name=p.get("product_name") or sku,
                    warehouse_location=p.get("warehouse_location"),
                    stock_quantity=stock_quantity,
                    sales_volume=sales_volume,
                    reorder_level=reorder_level,
                    last_unit_price=last_unit_price,
                    currency=p.get("currency") or "AUD",
                    status=status,
                    expiry_date=expiry,
                )
            )

        pending += 1
        if pending >= batch_size:
            await session.commit()
            pending = 0

    if pending:
        await session.commit()

async def main_async() -> None:
    parser = argparse.ArgumentParser(description="Seed demo data.")
    parser.add_argument("--force", action="store_true", help="Update seeded users (password/name).")
    parser.add_argument("--dry-run", action="store_true", help="Only load JSON and print counts (no DB writes).")
    parser.add_argument("--limit-products", type=int, default=None, help="Limit number of products to seed (testing).")
    args = parser.parse_args()

    try:
        categories_data = _load_json_list(JSON_CATEGORIES)
        suppliers_data = _load_json_list(JSON_SUPPLIERS)
        units_data = _units_seed_rows()
        products_data = _load_json_list(JSON_PRODUCTS)

        print(
            "[seed] JSON counts:",
            f"categories={len(categories_data)}",
            f"suppliers={len(suppliers_data)}",
            f"units={len(units_data)}",
            f"products={len(products_data)}",
        )

        if args.dry_run:
            print("[seed] dry-run enabled: skip DB writes.")
            return

        await seed_users(force=args.force)
        
        async with async_session_maker() as session:
            await seed_suppliers_from_json(session, force=args.force)
            category_id_by_name = await seed_categories_from_json(session, force=args.force)
            unit_id_by_name = await seed_units_from_json(session, force=args.force)
            base_unit_id = _first_seeded_unit_id(unit_id_by_name)
            if base_unit_id is None:
                raise RuntimeError(
                    f"No unit resolved for products; seed units from {JSON_UNITS} first "
                    "(need at least one row with unit_name)."
                )
            await seed_products_from_json(
                session,
                force=args.force,
                category_id_by_name=category_id_by_name,
                base_unit_id=base_unit_id,
                limit_products=args.limit_products,
            )

        print("Seed completed")
    except SQLAlchemyError as e:
        print("Seed failed (SQLAlchemyError):", e)
        raise

def main() -> None:
    asyncio.run(main_async())

if __name__ == "__main__":
    main()