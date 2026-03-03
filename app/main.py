from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .database import Base, engine
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import SessionLocal
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile, Depends
import pandas as pd
from .database import get_db
from . import models
from datetime import datetime
from fastapi import Body

Base.metadata.create_all(bind=engine)
app = FastAPI()

BASE_DIR = Path(__file__).parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")

# Страница логина
@app.get("/login", response_class=HTMLResponse)
async def login_page():
    return HTMLResponse((FRONTEND_DIR / "login.html").read_text(encoding="utf-8"))

fake_users = {"admin": "Password1"}

# Обработка логина
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username in fake_users and fake_users[username] == password:
        return RedirectResponse(url="/home", status_code=303)
    return HTMLResponse("<h3>Неверный логин или пароль</h3><a href='/login'>Назад</a>")

# Главная страница
@app.get("/home", response_class=HTMLResponse)
async def home():
    return HTMLResponse((FRONTEND_DIR / "index.html").read_text(encoding="utf-8"))

# Чтобы заход на / сразу редиректил на /login
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/login")


# Страница выхода (logout)
@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="session")
    return response

@app.get("/api/residents")
def get_residents():
    db: Session = SessionLocal()

    result = db.execute(text("SELECT * FROM residents_report"))
    rows = result.fetchall()

    data = []
    for row in rows:
        data.append({
            "field": row.field,
            "customer": row.customer,
            "full_name": row.full_name,
            "check_in": str(row.check_in),
            "check_out": str(row.check_out),
            "days": row.days
        })

    db.close()
    return JSONResponse(content=data)


def parse_date_dd_mm_yyyy(date_str):
    """
    Парсит дату из формата '11.01.2025' в datetime.date
    """
    if pd.isna(date_str):
        return None
    if isinstance(date_str, datetime):
        return date_str.date()  # если уже datetime
    try:
        return datetime.strptime(str(date_str).strip(), "%d.%m.%Y").date()
    except ValueError:
        return None

@app.post("/api/upload_excel")
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith((".xlsx", ".xls")):
        return {"error": "Неверный формат файла"}

    # Читаем Excel в pandas
    df = pd.read_excel(file.file)

    # Приводим названия колонок к нужным
    df.columns = [c.strip() for c in df.columns]

    for _, row in df.iterrows():
        # --- Работа с полем (месторождение) ---
        field_name = row["Месторождение"].strip()
        field = db.query(models.Field).filter(models.Field.name == field_name).first()
        if not field:
            field = models.Field(name=field_name)
            db.add(field)
            db.commit()
            db.refresh(field)

        # --- Работа с заказчиком ---
        customer_name = row["Заказчик"].strip()
        customer = db.query(models.Customer).filter(models.Customer.name == customer_name).first()
        if not customer:
            customer = models.Customer(name=customer_name)
            db.add(customer)
            db.commit()
            db.refresh(customer)

        # --- Добавляем проживающего ---
        resident = models.Resident(
            field_id=field.id,
            customer_id=customer.id,
            full_name=row["Фио проживающего"].strip(),
            check_in=parse_date_dd_mm_yyyy(row["Дата заезда"]),
            check_out=parse_date_dd_mm_yyyy(row["Дата выезда"]),
            days=int(row["Количество дней"])
        )
        db.add(resident)

    db.commit()
    return {"message": "Данные успешно загружены"}



@app.post("/api/add_resident")
def add_resident(data: dict = Body(...), db: Session = Depends(get_db)):

    try:
        field = db.query(models.Field).filter(
            models.Field.name == data["field"]
        ).first()

        if not field:
            field = models.Field(name=data["field"])
            db.add(field)
            db.commit()
            db.refresh(field)

        customer = db.query(models.Customer).filter(
            models.Customer.name == data["customer"]
        ).first()

        if not customer:
            customer = models.Customer(name=data["customer"])
            db.add(customer)
            db.commit()
            db.refresh(customer)

        resident = models.Resident(
            field_id=field.id,
            customer_id=customer.id,
            full_name=data["full_name"],
            check_in=datetime.strptime(data["check_in"], "%Y-%m-%d").date(),
            check_out=datetime.strptime(data["check_out"], "%Y-%m-%d").date(),
            days=int(data["days"])
        )

        db.add(resident)
        db.commit()

        return {"message": "Запись успешно добавлена"}

    except Exception as e:
        return {"error": str(e)}
