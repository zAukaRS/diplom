# test/conftest.py
import asyncio
import os
import tempfile
from io import BytesIO

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from openpyxl import Workbook
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.core.dependencies import get_current_user
from app.database import Base, get_db
from app.main import app as main_app
from app.models import Role, User, Field, Customer, Resident, Location, Path, Room, Request_before, Request


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    db_url = f"sqlite+aiosqlite:///{tmp.name}"
    engine = create_async_engine(db_url, echo=False, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()
    os.unlink(tmp.name)


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    async_session = async_sessionmaker(db_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()


# ---------- Инициализация ролей (один раз за сессию) ----------
@pytest_asyncio.fixture(scope="session")
async def init_roles(db_engine):
    async_session = async_sessionmaker(db_engine, expire_on_commit=False)
    async with async_session() as session:
        for role_name in ["user", "admin", "field_admin"]:
            result = await session.execute(select(Role).where(Role.name == role_name))
            role = result.scalars().first()
            if not role:
                session.add(Role(name=role_name))
        await session.commit()


# ---------- Роли (только получение) ----------
@pytest_asyncio.fixture
async def test_role_user(db_session, init_roles):
    result = await db_session.execute(select(Role).where(Role.name == "user"))
    return result.scalars().first()


@pytest_asyncio.fixture
async def test_role_admin(db_session, init_roles):
    result = await db_session.execute(select(Role).where(Role.name == "admin"))
    return result.scalars().first()


@pytest_asyncio.fixture
async def test_role_field_admin(db_session, init_roles):
    result = await db_session.execute(select(Role).where(Role.name == "field_admin"))
    return result.scalars().first()


# ---------- Пользователи (get-or-create) ----------
@pytest_asyncio.fixture
async def test_user(db_session, test_role_user):
    username = "testuser"
    result = await db_session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        user = User(username=username, password="hashed", role_id=test_role_user.id)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def admin_user(db_session, test_role_admin):
    username = "admin"
    result = await db_session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        user = User(username=username, password="hashed", role_id=test_role_admin.id)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def field_admin_user(db_session, test_role_field_admin, test_field):
    username = "fieldadmin"
    result = await db_session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        user = User(
            username=username,
            password="hashed",
            role_id=test_role_field_admin.id,
            field_id=test_field.id,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
    else:
        # Если пользователь уже существует, но поле не привязано – обновим
        if user.field_id is None:
            user.field_id = test_field.id
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)
    return user


# ---------- Доменные сущности (get-or-create) ----------
@pytest_asyncio.fixture
async def test_field(db_session):
    name = "Тестовое месторождение"
    result = await db_session.execute(select(Field).where(Field.name == name))
    field = result.scalars().first()
    if not field:
        field = Field(name=name)
        db_session.add(field)
        await db_session.commit()
        await db_session.refresh(field)
    return field


@pytest_asyncio.fixture
async def test_location(db_session):
    name = "Тестовое расположение"
    result = await db_session.execute(select(Location).where(Location.name == name))
    loc = result.scalars().first()
    if not loc:
        loc = Location(name=name)
        db_session.add(loc)
        await db_session.commit()
        await db_session.refresh(loc)
    return loc


@pytest_asyncio.fixture
async def test_path(db_session):
    description = "Тестовый путь"
    result = await db_session.execute(select(Path).where(Path.description == description))
    path = result.scalars().first()
    if not path:
        path = Path(description=description)
        db_session.add(path)
        await db_session.commit()
        await db_session.refresh(path)
    return path


@pytest_asyncio.fixture
async def test_room(db_session, test_field, test_location, test_path):
    room_number = "101"
    result = await db_session.execute(
        select(Room).where(Room.room_number == room_number, Room.field_id == test_field.id)
    )
    room = result.scalars().first()
    if not room:
        room = Room(
            room_number=room_number,
            field_id=test_field.id,
            capacity=2,
            location_id=test_location.id,
            path_id=test_path.id,
            room_unique_id="101a",
            status=0,
        )
        db_session.add(room)
        await db_session.commit()
        await db_session.refresh(room)
    return room


@pytest_asyncio.fixture
async def test_customer(db_session):
    name = "Тестовый заказчик"
    result = await db_session.execute(select(Customer).where(Customer.name == name))
    customer = result.scalars().first()
    if not customer:
        customer = Customer(name=name)
        db_session.add(customer)
        await db_session.commit()
        await db_session.refresh(customer)
    return customer


@pytest_asyncio.fixture
async def test_resident(db_session):
    full_name = "Тестовый Жилец"
    result = await db_session.execute(select(Resident).where(Resident.full_name == full_name))
    resident = result.scalars().first()
    if not resident:
        resident = Resident(
            full_name=full_name,
            position="Инженер",
            gender="М",
        )
        db_session.add(resident)
        await db_session.commit()
        await db_session.refresh(resident)
    return resident


# ---------- Автоматическая очистка заявок перед каждым тестом ----------
@pytest_asyncio.fixture(autouse=True)
async def clean_requests(db_session):
    # Удаляем все заявки, чтобы избежать накопления данных между тестами
    await db_session.execute(delete(Request_before))
    await db_session.execute(delete(Request))
    await db_session.commit()


# ---------- FastAPI клиент ----------
@pytest_asyncio.fixture
async def app(db_session):
    app = main_app

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    # Не переопределяем get_current_user — тесты сами задают нужного пользователя
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        ac.app = app  # для доступа к app в тестах
        yield ac


# ---------- Утилита для создания Excel ----------
def create_excel_file(rows, sheet_name="Sheet1"):
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name
    headers = ["Организация", "Договор", "ЕОЛ", "ФИО", "Должность", "Месторождение", "Заезд", "Выезд", "Дни"]
    ws.append(headers)
    for row in rows:
        ws.append(row)
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer