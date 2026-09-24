from sqlmodel import  SQLModel, create_engine, Session
from dotenv import load_dotenv
import os
from scripts.seed_users import seed_users

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_DB = os.getenv("DATABASE_DB")
DATABASE_PASS = os.getenv("DATABASE_PASS")

DATABASE_URL = f"postgresql+psycopg://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"

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
