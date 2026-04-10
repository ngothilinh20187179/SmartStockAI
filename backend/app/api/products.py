from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.core.database import get_session
from app.schemas.product import ProductListResponse
from app.services.product_service import list_products_service

router = APIRouter()


@router.get("/api/products", response_model=ProductListResponse)
async def list_products(
    q: str | None = Query(default=None, description="Search by name/sku/barcode"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session=Depends(get_session),
) -> ProductListResponse:
    return await list_products_service(session, q=q, limit=limit, offset=offset)

