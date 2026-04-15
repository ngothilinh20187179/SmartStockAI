from uuid import UUID, uuid4
from typing import Any, Optional
from decimal import Decimal
from datetime import date

from sqlalchemy import Column, Computed, Index
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlmodel import SQLModel, Field

from .enums import ProductStatus

_SEARCH_VECTOR_SQL = (
    "to_tsvector('simple', coalesce(product_name, '') || ' ' || "
    "coalesce(sku_code, '') || ' ' || "
    "coalesce(product_code, '') || ' ' || "
    "coalesce(barcode, ''))"
)

class Category(SQLModel, table=True):
    __tablename__ = "categories" # type: ignore
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    parent_id: Optional[UUID] = Field(default=None, foreign_key="categories.id")
    category_name: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)

class Unit(SQLModel, table=True):
    __tablename__ = "units" # type: ignore
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    unit_name: str = Field(max_length=50, nullable=False)
    unit_symbol: Optional[str] = Field(default=None, max_length=10)

class Product(SQLModel, table=True):
    __tablename__ = "products" # type: ignore
    __table_args__ = (
        Index(
            "ix_products_search_vector",
            "search_vector",
            postgresql_using="gin",
        ),
    )
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    category_id: Optional[UUID] = Field(default=None, foreign_key="categories.id")
    base_unit_id: Optional[UUID] = Field(default=None, foreign_key="units.id")
    sku_code: Optional[str] = Field(default=None, max_length=50, unique=True)
    barcode: Optional[str] = Field(default=None, max_length=100, unique=True)
    product_code: Optional[str] = Field(default=None, max_length=50, unique=True)
    product_name: str = Field(nullable=False)
    image_url: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    brand: Optional[str] = Field(default=None, max_length=100)
    stock_quantity: Decimal = Field(default=0, max_digits=15, decimal_places=2)
    sales_volume: Decimal = Field(default=0, max_digits=15, decimal_places=2)
    reorder_level: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    selling_price: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    last_unit_price: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    currency: str = Field(default="AUD", max_length=10)
    status: ProductStatus = Field(default=ProductStatus.in_stock)
    warehouse_location: Optional[str] = Field(default=None)
    is_batch_tracked: bool = Field(default=False)
    batch_number: Optional[str] = Field(default=None, max_length=50)
    expiry_date: Optional[date] = Field(default=None)
    search_vector: Optional[Any] = Field(
        default=None,
        exclude=True,
        sa_column=Column(
            TSVECTOR,
            Computed(_SEARCH_VECTOR_SQL, persisted=True),
            nullable=False,
        ),
    )

class ProductUnitConversion(SQLModel, table=True):
    __tablename__ = "product_unit_conversions" # type: ignore
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="products.id")
    unit_id: UUID = Field(foreign_key="units.id")
    factor: Decimal = Field(max_digits=15, decimal_places=4)