from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import SQLModel, Field
from .enums import SupplierStatus

class Supplier(SQLModel, table=True):
    __tablename__ = "suppliers" # type: ignore
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    supplier_name: str = Field(max_length=255, nullable=False)
    tax_code: Optional[str] = Field(default=None, max_length=50)
    supplier_code: Optional[str] = Field(default=None, max_length=50, unique=True)
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[str] = Field(default=None, max_length=100)
    website: Optional[str] = Field(default=None, max_length=255)
    address: Optional[str] = Field(default=None)
    bank_account_number: Optional[str] = Field(default=None, max_length=50)
    bank_name: Optional[str] = Field(default=None, max_length=100)
    logo: Optional[str] = Field(default=None)
    status: SupplierStatus = Field(default=SupplierStatus.active)