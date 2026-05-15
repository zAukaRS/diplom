from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path as PathLib

from app.core.dependencies import get_current_user
from app.models import User

router = APIRouter()
async def admin_only(user: User = Depends(get_current_user)):
    if user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    return user

BASE_DIR = PathLib(__file__).parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
templates = Jinja2Templates(directory=FRONTEND_DIR)

@router.get("/login", response_class=HTMLResponse)
async def login_page():
    return HTMLResponse((FRONTEND_DIR / "login.html").read_text(encoding="utf-8"))

@router.get("/home", response_class=HTMLResponse)
def home():
    return HTMLResponse((FRONTEND_DIR / "index.html").read_text(encoding="utf-8"))

@router.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/login")

@router.get("/admin_management", response_class=HTMLResponse)
def admin_page(request: Request, user: User = Depends(admin_only)):
    return templates.TemplateResponse("admin_management.html", {"request": request})