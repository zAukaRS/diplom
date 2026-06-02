from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path as PathLib
from starlette.templating import Jinja2Templates
from .routers import auth, users, pages, residents, days, excel, report, fields, customers, admins, current_user

app = FastAPI()

# uvicorn app.main:app --reload


# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(pages.router)
app.include_router(residents.router)
app.include_router(days.router)
app.include_router(excel.router)
app.include_router(report.router)
app.include_router(fields.router)
app.include_router(customers.router)
app.include_router(admins.router)
app.include_router(current_user.router)
# app.include_router(requests_router.router)

BASE_DIR = PathLib(__file__).parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
templates = Jinja2Templates(directory=FRONTEND_DIR)

app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")