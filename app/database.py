from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from pathlib import Path
import os
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv




load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")


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

