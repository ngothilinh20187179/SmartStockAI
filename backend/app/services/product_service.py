from __future__ import annotations

from sqlalchemy import func, or_
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.products import Category, Product, Unit
from backend.app.schemas.common import Pagination
from app.schemas.product import ProductListResponse, ProductRead


def _enum_value(v) -> str:
    return getattr(v, "value", str(v))


async def list_products_service(
    session: AsyncSession,
    *,
    q: str | None,
    limit: int,
    offset: int,
) -> ProductListResponse:
    q_norm = (q or "").strip()

    where = []
    if q_norm:
        like = f"%{q_norm}%"
        where.append(
            or_(
                Product.product_name.ilike(like),
                Product.sku_code.ilike(like),
                Product.product_code.ilike(like),
                Product.barcode.ilike(like),
            )
        )

    count_stmt = select(func.count(Product.id))
    if where:
        count_stmt = count_stmt.where(*where)
    total = int((await session.exec(count_stmt)).one())

    stmt = (
        select(Product, Category, Unit)
        .join(Category, Product.category_id == Category.id, isouter=True)
        .join(Unit, Product.base_unit_id == Unit.id, isouter=True)
        .order_by(Product.product_name.asc())
        .offset(offset)
        .limit(limit)
    )
    if where:
        stmt = stmt.where(*where)

    result = await session.exec(stmt)
    rows = result.all()

    items: list[ProductRead] = []
    for product, category, unit in rows:
        items.append(
            ProductRead(
                id=str(product.id),
                sku_code=product.sku_code,
                product_code=product.product_code,
                barcode=product.barcode,
                product_name=product.product_name,
                image_url=product.image_url,
                description=product.description,
                brand=product.brand,
                category_id=str(product.category_id) if product.category_id else None,
                category_name=category.category_name if category else None,
                base_unit_id=str(product.base_unit_id) if product.base_unit_id else None,
                unit_name=unit.unit_name if unit else None,
                unit_symbol=unit.unit_symbol if unit else None,
                stock_quantity=product.stock_quantity,
                sales_volume=product.sales_volume,
                reorder_level=product.reorder_level,
                selling_price=product.selling_price,
                last_unit_price=product.last_unit_price,
                currency=product.currency,
                status=_enum_value(product.status),
                warehouse_location=product.warehouse_location,
                is_batch_tracked=product.is_batch_tracked,
                batch_number=product.batch_number,
                expiry_date=product.expiry_date,
            )
        )

    return ProductListResponse(
        items=items,
        meta=Pagination(total=total, limit=limit, offset=offset),
    )

