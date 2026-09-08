from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path as PathLib
from starlette.templating import Jinja2Templates
from contextlib import asynccontextmanager
from sqlalchemy import select
from passlib.context import CryptContext

from .routers import auth, users, pages, residents, report, fields, customers, admins, current_user, requests as requests_router, excel, rooms_import
from .database import engine, async_session, Base
from .models import User, Role

# Контекст для хэширования паролей (используется при создании администратора)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Создание таблиц (идемпотентно)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2. Создание администратора, если его нет
    async with async_session() as session:
        # Проверяем/создаём роль "admin"
        stmt = select(Role).where(Role.name == "admin")
        admin_role = (await session.execute(stmt)).scalar_one_or_none()
        if not admin_role:
            admin_role = Role(name="admin")
            session.add(admin_role)
            await session.commit()

        # Проверяем пользователя "admin"
        stmt = select(User).where(User.username == "admin")
        admin_user = (await session.execute(stmt)).scalar_one_or_none()
        if not admin_user:
            # Хэшируем пароль admin123
            hashed = pwd_context.hash("Password1")
            admin_user = User(
                username="admin",
                password=hashed,
                role_id=admin_role.id,
                field_id=None,
                resident_id=None
            )
            session.add(admin_user)
            await session.commit()

    yield
    # Здесь можно добавить код завершения, если нужно


app = FastAPI(lifespan=lifespan)

# uvicorn app.main:app --reload

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(pages.router)
app.include_router(residents.router)
app.include_router(excel.router)
app.include_router(report.router)
app.include_router(fields.router)
app.include_router(customers.router)
app.include_router(admins.router)
app.include_router(current_user.router)
app.include_router(requests_router.router)
app.include_router(rooms_import.router)

BASE_DIR = PathLib(__file__).parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
templates = Jinja2Templates(directory=FRONTEND_DIR)

app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")