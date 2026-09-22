from uuid import UUID, uuid4
from enum import Enum
from datetime import UTC, datetime
from sqlmodel import Field, SQLModel, create_engine, Session
# from services.config import get_settings
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4,primary_key=True)
    email: str = Field(index=True, nullable=False, max_length=320)
    password_hash: str = Field(nullable=False)
    is_active: bool = Field(nullable=False, default=True)
    role: UserRole = Field(default=UserRole.USER)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = Field(default_factory=lambda: datetime.now(UTC))

# engine = create_engine(get_settings().database_url, echo=True)
engine = create_engine(DATABASE_URL, echo=True)


def create_tables() -> None:
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def close_db() -> None:
    """Dispose database connection pool."""
    engine.dispose()


def get_session():
    """Provide a database session per request."""
    with Session(engine) as session:
        yield session