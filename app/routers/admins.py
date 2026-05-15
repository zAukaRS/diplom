from fastapi import APIRouter, Depends, Request, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models import User, Role, Field
from app.core.security import get_password_hash
from app.core.dependencies import get_current_user
from app.utils import get_admin_role_id
from app.routers.pages import admin_only
router = APIRouter()



@router.get("/api/get_admins")
async def get_admins(db: AsyncSession = Depends(get_db), user: User = Depends(admin_only)):
    res = await db.execute(
        select(User)
        .join(Role, User.role_id == Role.id)
        .where(Role.name == 'admin')
        .options(selectinload(User.field))
    )
    admins = res.scalars().unique().all()
    result = []
    for u in admins:
        field_name = u.field.name if hasattr(u, "field") and u.field else ""
        result.append({"id": u.id, "username": u.username, "field": field_name})
    return result

@router.post("/api/create_admin")
async def create_admin(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(admin_only)
):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    field_id = data.get("field_id")
    if not username or not password:
        return JSONResponse({"error": "Все поля обязательны"}, status_code=400)

    res = await db.execute(select(User).where(User.username == username))
    if res.scalars().first():
        return JSONResponse({"error": "Логин уже существует"}, status_code=400)

    admin_role_id = await get_admin_role_id(db)
    hashed_password = get_password_hash(password)
    new_admin = User(
        username=username,
        password=hashed_password,
        role_id=admin_role_id,
        field_id=field_id if field_id else None,
    )
    db.add(new_admin)
    await db.commit()
    await db.refresh(new_admin)
    return {"message": f"Админ {username} создан!"}

@router.put("/api/update_admin_inline/{admin_id}")
async def update_admin_inline(
    admin_id: int,
    data: dict = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    try:
        res = await db.execute(select(User).where(User.id == admin_id))
        admin = res.scalars().first()
        if not admin:
            return JSONResponse({"error": "Админ не найден"}, status_code=404)
        if data.get("username"):
            admin.username = data["username"]
        if data.get("password"):
            admin.password = get_password_hash(data["password"])
        if data.get("field_id"):
            admin.field_id = data["field_id"]
        await db.commit()
        return {"message": "Обновлено"}
    except Exception as e:
        await db.rollback()
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)

@router.delete("/api/delete_admin/{admin_id}")
async def delete_admin(
    admin_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    try:
        res = await db.execute(select(User).where(User.id == admin_id))
        admin = res.scalars().first()
        if not admin:
            return JSONResponse({"error": "Админ не найден"}, status_code=404)
        await db.delete(admin)
        await db.commit()
        return {"message": "Админ удален"}
    except Exception as e:
        await db.rollback()
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)