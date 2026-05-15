from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User
from app.core.dependencies import get_current_user
from app.core.security import get_password_hash

router = APIRouter()

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Получение информации о текущем пользователе.
    Эндпоинт защищён: требуется валидный access токен.
    """
    return {"id": current_user.id, "username": current_user.username, "role_id": current_user.role_id}
