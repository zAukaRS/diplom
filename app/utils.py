from app.models import Role,ContractCounter
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import select

async def get_admin_role_id(db : AsyncSession):
    try:
        res = await db.execute(select(Role).where(Role.name == "admin"))
        role = res.scalars().first()
        if role:
            return role.id
        # Если роли нет, создаем
        new_role = Role(name="admin")
        db.add(new_role)
        await db.commit()
        await db.refresh(new_role)
        return new_role.id
    finally:
        await db.close()

async def generate_contract_number(db: AsyncSession, field_name: str) -> str:
    # Берём первые 3 буквы, заглавные, только кириллицу/латиницу (можно оставить как есть)
    prefix = field_name[:3].upper()
    
    # Ищем или создаём счётчик для этого префикса
    result = await db.execute(select(ContractCounter).where(ContractCounter.prefix == prefix))
    counter = result.scalars().first()
    if not counter:
        counter = ContractCounter(prefix=prefix, last_number=0)
        db.add(counter)
        await db.flush()
    
    # Увеличиваем номер
    new_number = counter.last_number + 1
    counter.last_number = new_number
    await db.flush()  # или commit позже
    
    return f"{prefix}-{new_number}"