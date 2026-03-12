from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field
from .enums import TransactionType

class StockLog(SQLModel, table=True):
    __tablename__ = "stock_log" # type: ignore
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="products.id")
    invoice_id: Optional[UUID] = Field(default=None, foreign_key="invoices.id")
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id")
    transaction_type: TransactionType = Field(nullable=False)
    quantity_change: Decimal = Field(max_digits=15, decimal_places=2)
    balance_after: Decimal = Field(max_digits=15, decimal_places=2)
    timestamp: datetime = Field(default_factory=datetime.now)