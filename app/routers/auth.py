from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from ..database import get_db
from sqlalchemy import select,and_,update
from ..models  import User,Refresh_Token
from ..schemas.token import Token
from ..core.security import verify_password, create_access_token, create_refresh_token, get_password_hash, decode_token
import hashlib
from ..core.dependencies import get_current_user
from datetime import datetime, timezone
router = APIRouter(prefix="/api/auth", tags=["authentication"])


class UserCreate(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Регистрация нового пользователя"""
    res = await db.execute(select(User).where(User.username == user_data.username))
    existing_user = res.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        password=hashed_password,
        role_id=2
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": f"Пользователь {new_user.username} создан", "id": new_user.id}




@router.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    
    """
    Аутентификация пользователя.
    Возвращает access и refresh токены.
    """
    res = await db.execute(select(User).where(User.username == form_data.username))
    user = res.scalars().first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    await db.execute(update(Refresh_Token)
    .where(Refresh_Token.user_id == user.id)
    .values(revoked = True)
    )
    await db.commit()
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()

    payload = decode_token(refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    exp_timestamp = payload.get("exp")
    expires_at = datetime.fromtimestamp(exp_timestamp)
    res = Refresh_Token(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at
    )
    db.add(res)
    await db.commit()
    await db.flush()


    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,          # для разработки (без HTTPS); в продакшене True
        samesite="lax",
        max_age=7 * 24 * 3600  # 7 дней
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """Обновление access токена с помощью refresh токена"""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    
   
    payload = decode_token(refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user = await db.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()

    res = await db.execute(select(Refresh_Token)
                           .where(and_(Refresh_Token.token_hash == token_hash,
                                        Refresh_Token.revoked == False,
                                        Refresh_Token.expires_at > datetime.now()
                                        )
                                )
                            )
    
    if not res.scalars().first():
        response.delete_cookie("refresh_token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    new_access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        await db.execute(update(Refresh_Token).where(Refresh_Token.token_hash == token_hash).values(revoked=True))
        await db.commit()
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}