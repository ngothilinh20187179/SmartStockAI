from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from backend.app.schemas.common import Pagination


class ProductRead(BaseModel):
    id: str
    sku_code: str | None
    product_code: str | None
    barcode: str | None
    product_name: str
    image_url: str | None
    description: str | None
    brand: str | None
    category_id: str | None
    category_name: str | None
    base_unit_id: str | None
    unit_name: str | None
    unit_symbol: str | None
    stock_quantity: Decimal
    sales_volume: Decimal
    reorder_level: Decimal | None
    selling_price: Decimal | None
    last_unit_price: Decimal | None
    currency: str
    status: str
    warehouse_location: str | None
    is_batch_tracked: bool
    batch_number: str | None
    expiry_date: date | None


class ProductListResponse(BaseModel):
    items: list[ProductRead]
    meta: Pagination

