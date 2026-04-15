from __future__ import annotations

from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.products import Category, Product, Unit
from app.schemas.common import Pagination
from app.schemas.product import ProductListResponse, ProductRead

from sqlalchemy import inspect

_products = inspect(Product).local_table 
_search_vector = _products.c.search_vector

_categories = inspect(Category).local_table
_units = inspect(Unit).local_table

def _enum_value(v) -> str:
    return getattr(v, "value", str(v))


async def list_products_service(
    session: AsyncSession,
    *,
    q: str | None,
    limit: int,
    offset: int,
) -> ProductListResponse:
    # 1. Normalize search query — use GIN-backed tsvector (see migration)
    q_norm = (q or "").strip()
    where_clauses = []
    tsq = None

    if q_norm:
        search_terms = [f"{word}:*" for word in q_norm.split() if word]
        if search_terms:
            query_string = " & ".join(search_terms)
            tsq = func.to_tsquery("simple", query_string)
            where_clauses.append(_search_vector.op("@@")(tsq))

    # 2. Count Total Records (Optimize by only selecting count)
    count_stmt = select(func.count(_products.c.id)).select_from(_products)
    if where_clauses:
        count_stmt = count_stmt.where(*where_clauses)
    
    total_result = await session.exec(count_stmt)
    total = total_result.one()

    # 3. Fetch Data with Joins
    stmt = (
    select(Product, Category, Unit)
        .join(Category, _products.c.category_id == _categories.c.id, isouter=True)
        .join(Unit, _products.c.base_unit_id == _units.c.id, isouter=True)
    )

    if where_clauses:
        assert tsq is not None
        stmt = stmt.where(*where_clauses)
        # Order by relevance when search query is present
        stmt = stmt.order_by(func.ts_rank(_search_vector, tsq).desc())
    else:
        stmt = stmt.order_by(_products.c.product_name.asc())

    stmt = stmt.offset(offset).limit(limit)

    result = await session.exec(stmt)
    rows = result.all()

    # 4. Map Results to Schema
    items: list[ProductRead] = []
    for product, category, unit in rows:
        product_data = product.model_dump()
        product_data.update({
            "id": str(product.id),
            "category_id": str(product.category_id) if product.category_id else None,
            "category_name": category.category_name if category else None,
            "base_unit_id": str(product.base_unit_id) if product.base_unit_id else None,
            "unit_name": unit.unit_name if unit else None,
            "unit_symbol": unit.unit_symbol if unit else None,
            "status": _enum_value(product.status),
        })
        items.append(ProductRead.model_validate(product_data))

    return ProductListResponse(
        items=items,
        meta=Pagination(total=total, limit=limit, offset=offset),
    )