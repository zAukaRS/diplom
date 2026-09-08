from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Добавляем параметр foreign_keys=on прямо в URL (по умолчанию)
default_db_url = "sqlite+aiosqlite:///./database.db?foreign_keys=on"
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", default_db_url)

Base = declarative_base()

# Для SQLite оставляем только check_same_thread (если нужно),
# foreign_keys теперь задаётся через URL
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False}  # только этот параметр
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with async_session() as db:
        yield db