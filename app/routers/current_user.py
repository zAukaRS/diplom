from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.models import User

router = APIRouter()

@router.get("/api/current_user")
def current_user(user: User = Depends(get_current_user)):
    return {"username": user.username, "role": user.role.name}