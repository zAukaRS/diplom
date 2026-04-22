from .models import Role
from .database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import select

async def get_admin_role_id(db : AsyncSession = Depends(get_db)):
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
        db.close()