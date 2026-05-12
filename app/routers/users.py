from fastapi import APIRouter, Depends
from ..core.dependencies import get_current_user
from ..models import User

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me", response_model=User)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Получение информации о текущем пользователе.
    Эндпоинт защищён: требуется валидный access токен.
    """
    return current_user