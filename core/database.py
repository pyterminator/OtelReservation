import os
from dotenv import load_dotenv
# from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

load_dotenv()

DB_HOST: str = os.getenv("DB_HOST")
DB_PORT: int = os.getenv("DB_PORT")
DB_USER: str = os.getenv("DB_USER")
DB_NAME: str = os.getenv("DB_NAME")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")

# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# engine = create_engine(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True)

BASE = declarative_base()

# SessionLocal = sessionmaker(bind=engine, autoflush=True)
# db_session = SessionLocal()

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# alembic revision --autogenerate -m "add role to users"