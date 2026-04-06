from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .database import Base, engine
from sqlalchemy.orm import Session
from sqlalchemy import text,or_,and_
from .database import SessionLocal
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile, Depends
import pandas as pd
from .database import get_db
from . import models
from datetime import datetime,timedelta, date
from fastapi import Body
import os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


# uvicorn app.main:app --reload

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
def get_residents(db: Session = Depends(get_db)):
    residents = db.query(models.Resident).all()
    data = []

    for r in residents:
        room = r.room
        location = room.location if room else None
        path = room.path if room else None
        field = r.field
        customer = r.customer

        days_info = {}
        for rd in r.resident_days:
            day = rd.date.day
            days_info[day] = rd.workplace_id

        data.append({
            "id": r.id,
            "room_number": room.room_number if room else "",
            "room_location": location.name if location else "",
            "room_path": path.description if path else "",
            "full_name": r.full_name,
            "position": r.position or "",
            "gender": r.gender or "",
            "field": field.name if field else "",
            "customer": customer.name if customer else "",
            "days_info": days_info,

        })

    return JSONResponse(content=data)


def parse_date_dd_mm_yyyy(date_str):

    if pd.isna(date_str):
        return None
    if isinstance(date_str, datetime):
        return date_str.date()
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

    df.columns = [c.strip() for c in df.columns]

    for _, row in df.iterrows():
        field_name = row["Месторождение"].strip()
        field = db.query(models.Field).filter(models.Field.name == field_name).first()
        if not field:
            field = models.Field(name=field_name)
            db.add(field)
            db.commit()
            db.refresh(field)

        customer_name = row["Заказчик"].strip()
        customer = db.query(models.Customer).filter(models.Customer.name == customer_name).first()
        if not customer:
            customer = models.Customer(name=customer_name)
            db.add(customer)
            db.commit()
            db.refresh(customer)

        resident = models.Resident(
            field_id=field.id,
            customer_id=customer.id,
            full_name=row["Фио проживающего"].strip(),
            position=row.get("Должность", "").strip(),
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
        # --- Работа с полем (месторождение) ---
        field = db.query(models.Field).filter(
            models.Field.name == data["field"]
        ).first()
        if not field:
            field = models.Field(name=data["field"])
            db.add(field)
            db.commit()
            db.refresh(field)

        # --- Работа с заказчиком ---
        customer = db.query(models.Customer).filter(
            models.Customer.name == data["customer"]
        ).first()
        if not customer:
            customer = models.Customer(name=data["customer"])
            db.add(customer)
            db.commit()
            db.refresh(customer)

        # --- Добавляем проживающего ---
        resident = models.Resident(
            field_id=field.id,
            customer_id=customer.id,
            full_name=data["full_name"],
            position=data.get("position", ""),
            check_in=datetime.strptime(data["check_in"], "%Y-%m-%d").date(),
            check_out=datetime.strptime(data["check_out"], "%Y-%m-%d").date(),
            days=int(data["days"])
        )
        db.add(resident)
        db.commit()
        db.refresh(resident)

        current = resident.check_in
        while current <= resident.check_out:
            day = models.ResidentDay(
                resident_id=resident.id,
                date=current
            )
            db.add(day)
            current += timedelta(days=1)
        db.commit()

        return {"message": "Запись успешно добавлена"}

    except Exception as e:
        return {"error": str(e)}


@app.get("/api/fields")
def get_fields(db: Session = Depends(get_db)):

    fields = db.query(models.Field).all()

    return [
        {"id": f.id, "name": f.name}
        for f in fields
    ]

@app.get("/api/workplaces")
def get_workplaces(db: Session = Depends(get_db)):
    workplaces = db.query(models.Workplace).all()
    return [{"id": w.id, "name": w.name} for w in workplaces]




@app.post("/api/update_day")
def update_day(data: dict = Body(...), db: Session = Depends(get_db)):
    try:
        resident_id = int(data["resident_id"])
        day = int(data["day"])
        month = int(data["month"])
        year = int(data["year"])

        workplace_id = data.get("workplace_id")
        try:
            workplace_id = int(workplace_id)
        except (TypeError, ValueError):
            workplace_id = None

        target_date = date(year, month, day)

        rd = db.query(models.ResidentDay).filter(
            models.ResidentDay.resident_id == resident_id,
            models.ResidentDay.date == target_date
        ).first()

        if workplace_id is None:
            # Удаляем запись, если пусто
            if rd:
                db.delete(rd)
                db.commit()
            return JSONResponse({"status": "deleted"})
        else:
            # Создаём или обновляем
            if not rd:
                rd = models.ResidentDay(
                    resident_id=resident_id,
                    date=target_date,
                    workplace_id=workplace_id
                )
                db.add(rd)
            else:
                rd.workplace_id = workplace_id
            db.commit()
            return JSONResponse({"status": "saved"})

    except Exception as e:
        db.rollback()
        return JSONResponse({"status": "error", "detail": str(e)})
    



def create_report(dict_list: list, output_filename: str, sheet_name='расч.л'):

    if not os.path.exists('excel_files'):
        os.makedirs('excel_files')

    filepath = os.path.join('excel_files', output_filename)

    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    headers = ['Месторождение', 'Заказчик', 'ФИО проживающего',
               'Дата заезда', 'Дата выезда', 'Количество дней']

    # добавляем данные
    ws.append(headers)

    for row in dict_list:
        ws.append([
            row['Месторождение'],
            row['Заказчик'],
            row['ФИО проживающего'],
            row['Дата заезда'].strftime("%d.%m.%Y"),
            row['Дата выезда'].strftime("%d.%m.%Y") if row['Дата выезда'] else "—",
            row['Количество дней']
        ])

    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Заголовки
    for cell in ws[1]:
        cell.font = Font(bold=True, name="Times New Roman", size=11)
        cell.fill = PatternFill("solid", fgColor="CCCCCC")
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border

    # Данные
    for row in ws.iter_rows(min_row=2):
        for i, cell in enumerate(row, start=1):
            cell.font = Font(name="Times New Roman", size=11)
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border

            if i in (4, 5, 6):
                cell.fill = PatternFill(start_color="86D472", end_color="86D472", fill_type="solid")

    widths = [25, 25, 30, 15, 15, 20]

    for i, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = width

    wb.save(filepath)
    return filepath



@app.get('/api/get_report')
def get_report(date_from : date, date_to : date, db: Session = Depends(get_db)):
    
    # print(f"Ищем за период: {date_from} — {date_to}") 

    residents = db.query(models.Resident).join(models.Field).join(models.Customer)\
        .filter(and_(
                models.Resident.check_in <= date_to,
                models.Resident.check_out >= date_from )
        ).order_by(
            models.Field.name,
            models.Customer.name,
        ).all()

    # print(f"Найдено жильцов: {len(residents)}")  

    if not residents:
        return JSONResponse({"error": "Нет данных за выбранный месяц"}, status_code=404)
    f = [{
        'Месторождение': r.field.name,
        'Заказчик': r.customer.name,
        'ФИО проживающего': r.full_name,
        'Дата заезда': r.check_in,
        'Дата выезда': r.check_out if r.check_out <= date_to else None,
        'Количество дней': len(r.resident_days) if r.check_out <= date_to else (date_to-r.check_in).days + 1
    } for r in residents]

    
    file_path = create_report(f, f"report_sine{date_from.month}.xlsx")
    return FileResponse(file_path, filename=file_path)