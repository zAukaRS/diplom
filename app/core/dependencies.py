from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import selectinload
from ..database import get_db
from ..models import User 
from .security import decode_token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession  = Depends(get_db)
) -> User:
    """
    Зависимость, которая извлекает текущего пользователя из токена.
    Используется для защиты эндпоинтов.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    try:
        user_id = int(user_id)
    except ValueError:
        raise credentials_exception

    res = await db.execute(select(User).where(User.id == user_id).options(selectinload(User.role)))
    res = await db.execute(select(User).where(User.id == user_id).options(selectinload(User.role)))
    user = res.scalars().first()
    if user is None:
        raise credentials_exception
    
    return user
