from sqlmodel import  SQLModel, create_engine, Session
from dotenv import load_dotenv
import os
from scripts.seed_users import seed_users

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# engine = create_engine(get_settings().database_url, echo=True)
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    """Provide a database session per request."""
    with Session(engine) as session:
        yield session

def create_tables() -> None:
    """Create database tables and load schema data."""
    # Create tables using SQLModel
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        seed_users(session)


def close_db() -> None:
    """Dispose database connection pool."""
    engine.dispose()
