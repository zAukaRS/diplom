from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from starlette.templating import Jinja2Templates
from werkzeug.security import generate_password_hash
from .utils import get_admin_role_id
from sqlalchemy.orm import selectinload 
from sqlalchemy import text, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile, Depends
import pandas as pd
from .database import get_db, Session_async
from . import models
from datetime import datetime,timedelta, date
from fastapi import Body
import os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from werkzeug.security import check_password_hash
from typing import Dict, List, Optional
from .models import User, Role
from sqlalchemy.orm import joinedload
from sqlalchemy import text, and_, or_, select, func, desc, extract, and_
from fastapi import Depends, HTTPException


# uvicorn app.main:app --reload


app = FastAPI()


BASE_DIR = Path(__file__).parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
templates = Jinja2Templates(directory=FRONTEND_DIR)

app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")


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

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    session_username = request.cookies.get("session")
    if not session_username:
        raise HTTPException(status_code=401, detail="Не авторизован")
    res = await db.execute(select(models.User).where(models.User.username == session_username))
    user = res.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user



def admin_only(user: models.User = Depends(get_current_user)):
    if user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    return user



def parse_date_dd_mm_yyyy(date_str):

    if pd.isna(date_str):
        return None
    if isinstance(date_str, datetime):
        return date_str.date()
    try:
        return datetime.strptime(str(date_str).strip(), "%d.%m.%Y").date()
    except ValueError:
        return None


def search(word : str, data : list):
    word = word.lower()
    filters = ['full_name','position','room_number','field','room_location']
    for i in filters:
        res = [{"id": r.id,
                "room_number": r.room_number or "",
                "room_location": r.room_location or "",
                "room_path": r.room_path or "",
                "full_name": r.full_name ,
                "position": r.position or "",
                "gender": r.gender or "",
                "shift": r.shift or "",
                "field": r.field ,
                "customer": r.customer,
                "days_info": r.days_info} for r in data if r[i] == f'{word}%']
        if res:
            return res


@app.get("/login", response_class=HTMLResponse)
async def login_page():
    return HTMLResponse((FRONTEND_DIR / "login.html").read_text(encoding="utf-8"))

fake_users = {"admin": "Password1"}

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(models.User).where(models.User.username == username))
    user = res.scalars().first()
    if not user or not check_password_hash(user.password, password):
        return HTMLResponse("<h3>Неверный логин или пароль</h3><a href='/login'>Назад</a>")

    response = RedirectResponse(url="/home", status_code=303)
    response.set_cookie(
        key="session",
        value=user.username,
        httponly=True,
        max_age=3600
    )
    return response

# Главная страница
@app.get("/home", response_class=HTMLResponse)
def home():
    return HTMLResponse((FRONTEND_DIR / "index.html").read_text(encoding="utf-8"))

# Чтобы заход на / сразу редиректил на /login
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/login")


# Страница выхода (logout)
@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="session")
    return response


@app.post("/api/update_day")
async def update_day(data: dict = Body(...), db: AsyncSession = Depends(get_db)):
    try:
        resident_id = int(data["resident_id"])
        day = int(data["day"])
        month = int(data["month"])
        year = int(data["year"])

        # Обработка workplace_id безопасно
        workplace_id = data.get("workplace_id")
        try:
            workplace_id = int(workplace_id)
        except (TypeError, ValueError):
            workplace_id = None

        target_date = date(year, month, day)
        res = await db.execute(select(models.ResidentDay).where(and_(models.ResidentDay.resident_id == resident_id,models.ResidentDay.date == target_date)))
        rd = res.scalars().first()
        if not rd:
            rd = models.ResidentDay(
                resident_id=resident_id,
                date=target_date,
                workplace_id=workplace_id
            )
            db.add(rd)
        else:
            rd.workplace_id = workplace_id

        await db.commit()
        return JSONResponse({"status": "ok"})

    except Exception as e:
        await db.rollback()
        return JSONResponse({"status": "error", "detail": str(e)})
    




@app.get("/api/residents")
async def get_residents(
    word: Optional[str] = None, 
    by_field: Optional[str] = None, 
    db: AsyncSession = Depends(get_db)
):
    
    
    query = select(models.Resident).options(
        selectinload(models.Resident.field),
        selectinload(models.Resident.customer),
        selectinload(models.Resident.room).selectinload(models.Room.location),
        selectinload(models.Resident.room).selectinload(models.Room.path),
        selectinload(models.Resident.resident_days)
    )
    
    # Фильтр по ID месторождения
    if by_field and by_field.strip():
        try:
            field_id = int(by_field)
            query = query.where(models.Resident.field_id == field_id)
            print(f"  Фильтр по field_id: {field_id}")
        except ValueError:
            pass
    
    # Фильтр по поисковому слову
    if word:
        word_lower = word.lower().strip()
        query = query.outerjoin(models.Room)\
                     .outerjoin(models.Location)\
                     .outerjoin(models.Customer)\
                     .where(
            or_(
                models.Resident.full_name.ilike(f"%{word_lower}%"),
                models.Resident.position.ilike(f"%{word_lower}%"),
                models.Room.room_number.ilike(f"%{word_lower}%"),
                models.Location.name.ilike(f"%{word_lower}%"),
                models.Customer.name.ilike(f"%{word_lower}%")
            )
        )

    
    # Выполняем запрос
    result = await db.execute(query)
    residents = result.scalars().unique().all()
    
   
    
    if not residents:
        return []
    
    # Формируем ответ
    response = []
    for r in residents:
        room = r.room
        location = room.location if room else None
        
        days_info = {}
        for rd in r.resident_days:
            days_info[rd.date.day] = rd.workplace_id
        
        response.append({
            "id": r.id,
            "full_name": r.full_name,
            "position": r.position or "",
            "gender": r.gender or "",
            "shift": r.shift or "",
            "room_number": room.room_number if room else "",
            "room_location": location.name if location else "",
            "room_path": room.path.description if room and room.path else "",
            "room_capacity": "",
            "field": r.field.name if r.field else "",
            "customer": r.customer.name if r.customer else "",
            "days_info": days_info
        })
    
    
    return response
@app.post("/api/add_resident")
async def add_resident(data: dict = Body(...), db: AsyncSession = Depends(get_db)):
    try:
        res = await db.execute(select(models.Field).where(models.Field.name == data["field"]))
        field = res.scalars().first()
        if not field:
            field = models.Field(name=data["field"])
            db.add(field)
            await db.flush()

        # --- Работа с заказчиком ---
        res = await db.execute(select(models.Customer).where( models.Customer.name == data["customer"]))
        customer = res.scalars().first()
           
        if not customer:
            customer = models.Customer(name=data["customer"])
            db.add(customer)
            await db.flush()

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
        await db.flush()

        current = resident.check_in
        while current <= resident.check_out:
            day = models.ResidentDay(
                resident_id=resident.id,
                room_id=resident.room_id if resident.room_id else None,
                date=current
            )
            db.add(day)
            current += timedelta(days=1)
        await db.commit()
        await db.refresh(resident)
        return {"message": "Запись успешно добавлена", "resident_id": resident.id}

    except Exception as e:
        await db.rollback()
        return {"error": str(e)}
    
@app.post("/api/upload_excel")
async def upload_excel(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename.endswith((".xlsx", ".xls")):
        return {"error": "Неверный формат файла"}

    # Читаем Excel в pandas
    contents = await file.read()
    df = pd.read_excel(pd.io.excel.ExcelFile(contents))

    df.columns = [c.strip() for c in df.columns]

    for _, row in df.iterrows():
        field_name = row["Месторождение"].strip()
        res = await db.execute(select(models.Field).where(models.Field.name == field_name))
        field = res.scalars().first()
        if not field:
            field = models.Field(name=field_name)
            db.add(field)
            await db.flush()

        customer_name = row["Заказчик"].strip()
        res = await db.execute(select(models.Customer).where(models.Customer.name == customer_name))
        customer = res.scalars().first()
        if not customer:
            customer = models.Customer(name=customer_name)
            db.add(customer)
            await db.flush()

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

    await db.commit()
    return {"message": "Данные успешно загружены"}




@app.get('/api/get_report')
async def get_report(date_in : date, date_out : date, db: AsyncSession = Depends(get_db)):
    
    # print(f"Ищем за период: {date_from} — {date_to}") 
    res = await db.execute(
                            select(models.Resident)
                           .join(models.Field, models.Field.id == models.Resident.field_id)
                           .join(models.Customer, models.Customer.id == models.Resident.customer_id)
                           .where(and_(models.Resident.check_in <= date_out,
                                       models.Resident.check_out >= date_in))
                            .order_by(models.Field.name, models.Customer.name)
                            .options(
                            selectinload(models.Resident.field),      # ← загружаем field
                            selectinload(models.Resident.customer)   # ← загружаем customer
                            )
                        )
    residents = res.scalars().unique().all()
    # print(f"Найдено жильцов: {len(residents)}")  

    if not residents:
        return JSONResponse({"error": "Нет данных за выбранный период"}, status_code=404)

    f = []
    for r in residents:
        actual_in = r.check_in if r.check_in >= date_in else date_in
        actual_out = r.check_out if r.check_out and r.check_out <= date_out else date_out
        days = (actual_out - actual_in).days + 1

        f.append({
            'Месторождение': r.field.name,
            'Заказчик': r.customer.name,
            'ФИО проживающего': r.full_name,
            'Дата заезда': actual_in,
            'Дата выезда': actual_out,
            'Количество дней': days
        })
    
    file_path = create_report(f, f"report_{date_in}_{date_out}.xlsx")
    return FileResponse(file_path, filename=os.path.basename(file_path))



@app.get("/api/workplaces")
async def get_workplaces(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(models.Workplace))
    workplaces = res.scalars().all()
    return [{"id": w.id, "name": w.name} for w in workplaces]

@app.get("/api/fields")
async def get_fields(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Field))
    fields = result.scalars().all()
    return [
        {"id": f.id, "name": f.name}
        for f in fields
    ]


@app.get("/api/current_user")
def current_user(user: User = Depends(get_current_user)):
    return {"username": user.username, "role": user.role.name}

@app.get("/admin_management", response_class=HTMLResponse)
def admin_page(request: Request, user: User = Depends(admin_only)):
    return templates.TemplateResponse("admin_management.html", {"request": request})

@app.get("/api/get_admins")
async def get_admins(db: AsyncSession = Depends(get_db), user: User = Depends(admin_only)):
    res = await db.execute(select(models.User)
                           .join(models.Role, models.User.role_id == models.Role.id)
                           .where(models.Role.name == 'admin')
                           .options(selectinload(models.User.field)) )
    admins = res.scalars().unique().all()
    result = []
    for u in admins:
        # добавляем поле "field" если оно есть, иначе None
        field_name = u.field.name if hasattr(u, "field") and u.field else ""
        result.append({
            "id": u.id,
            "username": u.username,
            "field": field_name
        })
    return result

@app.post("/api/create_admin")
async def create_admin(request: Request, user: User = Depends(admin_only), db : AsyncSession = Depends(get_db)): ###############################################
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    field_id = data.get("field_id")
    if not username or not password:
        return JSONResponse({"error": "Все поля обязательны"}, status_code=400)

    # Я ТУТ ХЗ ЧТО ЭТО ЗА ПЕРЕМЕННАЯ Я ПЛОХО СДЕЛАЛ РАНЬШЕ БЫЛ Sessionlocal
    res = await db.execute(select(models.User).where(models.User.username == username))
    if res.scalars().first():
        return JSONResponse({"error": "Логин уже существует"}, status_code=400)

    admin_role_id = await get_admin_role_id(db)
    hashed_password = generate_password_hash(password)

    new_admin = models.User(
        username=username,
        password=hashed_password,
        role_id=admin_role_id,
        field_id=field_id if field_id else None,
    )
    db.add(new_admin)
    await db.commit()
    await db.refresh(new_admin)
    return {"message": f"Админ {username} создан!"}
    








@app.put("/api/update_admin_inline/{admin_id}")
async def update_admin_inline(admin_id: int, data: dict = Body(...), db : AsyncSession = Depends(get_db), current_user: User = Depends(admin_only)): ##############################
    try:
        res = await db.execute(select(models.User).where(models.User.id == admin_id))
        admin = res.scalars().first()
        if not admin:
            return JSONResponse({"error": "Админ не найден"}, status_code=404)

        if data.get("username"):
            admin.username = data["username"]
        if data.get("password"):
            admin.password = generate_password_hash(data["password"])
        if data.get("field_id"):
            admin.field_id = data["field_id"]

        await db.commit()
        return {"message": "Обновлено"}
    except  Exception as e:
        await db.rollback()
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)
    


@app.delete("/api/delete_admin/{admin_id}")
async def delete_admin(admin_id: int, db : AsyncSession = Depends(get_db), current_user: User = Depends(admin_only)):
    try:
        res = await db.execute(select(models.User).where(models.User.id == admin_id))
        admin = res.scalars().first()
        if not admin:
            return JSONResponse({"error": "Админ не найден"}, status_code=404)
        db.delete(admin)
        await db.commit()
        return {"message": "Админ удален"}
    except  Exception as e:
        await db.rollback()
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)


@app.post("/api/update_resident")
async def update_resident(data: dict = Body(...), db: AsyncSession = Depends(get_db)):
    try:
        res = await db.execute(select(models.Resident).where(models.Resident.id == data["id"]))
        resident = res.scalars().first()
        if not resident:
            return JSONResponse(content={"error": "Жилец не найден"}, status_code=404)

        if "position" in data:
            resident.position = data["position"]
        if "gender" in data:
            resident.gender = data["gender"]
        if "shift" in data:
            resident.shift = data["shift"]

        await db.commit()
        await db.refresh(resident)
        return JSONResponse(content={"status": "ok"})
    except Exception as e:
        await db.rollback()
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)


@app.get("/api/customers")
async def get_customers(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(models.Customer))
    customers = res.scalars().all()
    return [{"id": c.id, "name": c.name} for c in customers]
