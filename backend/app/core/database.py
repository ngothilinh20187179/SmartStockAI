import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "my_very_secure_password_123")
DB_NAME = os.getenv("POSTGRES_DB", "smartstock_db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

DB_HOST = os.getenv("DB_HOST", "localhost")

DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
