from uuid import UUID, uuid4
from typing import Optional
from decimal import Decimal
from datetime import date
from sqlmodel import SQLModel, Field
from .enums import PaymentStatus, InvoiceStatus

class Invoice(SQLModel, table=True):
    __tablename__ = "invoices" # type: ignore
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    supplier_id: Optional[UUID] = Field(default=None, foreign_key="suppliers.id")
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id")
    file_name: Optional[str] = Field(default=None)
    file_size: Optional[int] = Field(default=None)
    file_type: Optional[str] = Field(default=None, max_length=50)
    ocr_raw_text: Optional[str] = Field(default=None)
    invoice_url: Optional[str] = Field(default=None)
    invoice_code: Optional[str] = Field(default=None, max_length=100)
    invoice_date: Optional[date] = Field(default=None)
    currency: str = Field(default="AUD", max_length=10)
    sub_total: Decimal = Field(default=0, max_digits=15, decimal_places=2)
    total_tax: Decimal = Field(default=0, max_digits=15, decimal_places=2)
    total_amount: Decimal = Field(default=0, max_digits=15, decimal_places=2)
    payment_status: PaymentStatus = Field(default=PaymentStatus.unpaid)
    invoice_status: InvoiceStatus = Field(default=InvoiceStatus.pending)
    error_message: Optional[str] = Field(default=None)

class InvoiceItem(SQLModel, table=True):
    __tablename__ = "invoice_items" # type: ignore
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    invoice_id: UUID = Field(foreign_key="invoices.id")
    product_id: Optional[UUID] = Field(default=None, foreign_key="products.id")
    raw_product_name: Optional[str] = Field(default=None)
    quantity: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    unit: Optional[str] = Field(default=None, max_length=50)
    unit_price: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    line_total: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    confidence_score: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=2)
    has_gst: bool = Field(default=True)