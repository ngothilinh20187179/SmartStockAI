from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import SQLModel, Field
from .enums import UserStatus, UserRole

class User(SQLModel, table=True):
    __tablename__ = "users" # type: ignore
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_name: str = Field(max_length=100, nullable=False)
    hash_password: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.staff)
    email: Optional[str] = Field(default=None, max_length=255, unique=True)
    status: UserStatus = Field(default=UserStatus.active)