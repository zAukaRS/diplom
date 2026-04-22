from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
import os
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"  # поднимаемся на 2 уровня до D:\diplom
load_dotenv(env_path)
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
Base = declarative_base()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True)


Session_async = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with Session_async () as db:
        yield db

