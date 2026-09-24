from uuid import UUID, uuid4
from enum import Enum
from datetime import UTC, datetime
from sqlmodel import Field, SQLModel

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4,primary_key=True)
    email: str = Field(index=True, nullable=False, max_length=50)
    password_hash: str = Field(nullable=False)
    is_active: bool = Field(nullable=False, default=True)
    role: UserRole = Field(default=UserRole.USER)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))