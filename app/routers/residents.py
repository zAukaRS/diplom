
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from datetime import datetime, date,timedelta
from typing import Optional
from app.database import get_db
from app.models import Resident, Field, Customer, Location, Path, Room, ResidentDay
from app.core.dependencies import get_current_user

router = APIRouter()

def days_in_month(year: int, month: int) -> int:
    if month == 12:
        return 31
    return (date(year, month + 1, 1) - timedelta(days=1)).day

@router.get("/api/residents")
async def get_residents(
    word: Optional[str] = None,
    by_field: Optional[str] = None,
    month: Optional[int] = None,       
    year: Optional[int] = None,
    limit: int = 30,          
    offset: int = 0,   
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),
):  
    current_date_time = datetime.now()
    if month is None:
        month = current_date_time.month
    if year is None:
        year = current_date_time.year
    
    month_start = date(year, month, 1)
    month_end = date(year, month, days_in_month(year, month))
    
    # Основной запрос: только жильцы, у которых есть пересечение с месяцем
    query = select(Resident).options(
        selectinload(Resident.field),
        selectinload(Resident.customer),
        selectinload(Resident.room).selectinload(Room.location),
        selectinload(Resident.room).selectinload(Room.path),
        selectinload(Resident.resident_days).selectinload(ResidentDay.workplace)
    ).join(Resident.resident_days).where(
        and_(
            ResidentDay.date <= month_end,
            ResidentDay.extra >= month_start
        )
    ).distinct()

    if by_field and by_field.strip():
        try:
            field_id = int(by_field)
            query = query.where(Resident.field_id == field_id)
        except ValueError:
            pass

    if word:
        word_lower = word.lower().strip()
        # Явно присоединяем нужные таблицы с условиями
        query = query.outerjoin(Room, Resident.room_id == Room.id)
        query = query.outerjoin(Location, Room.location_id == Location.id)
        query = query.outerjoin(Customer, Resident.customer_id == Customer.id)  # через Resident, не через ResidentDay
        query = query.where(
            or_(
                Resident.full_name.ilike(f"%{word_lower}%"),
                Resident.position.ilike(f"%{word_lower}%"),
                Room.room_number.ilike(f"%{word_lower}%"),
                Location.name.ilike(f"%{word_lower}%"),
                Customer.name.ilike(f"%{word_lower}%")
            )
        )

    query = query.limit(limit).offset(offset)   # добавить пагинацию
    result = await db.execute(query)
    residents = result.scalars().unique().all()
    if not residents:
        return []

    response = []
    for r in residents:
        room = r.room
        location = room.location if room else None
        workplace_name = None
        days_info = {}
        
        for rd in r.resident_days:
            start = max(rd.date, month_start)
            end = min(rd.extra, month_end)
            if start <= end:
                delta = (end - start).days + 1
                if rd.workplace:
                    workplace_name = rd.workplace.name
                for d in range(delta):
                    day_num = (start + timedelta(days=d)).day
                    days_info[day_num] = rd.customer_id
        
        response.append({
            "id": r.id,
            "full_name": r.full_name,
            "position": r.position or "",
            "gender": r.gender or "",
            "shift": r.shift or "",
            "room_number": room.room_number if room else "",
            "room_location": location.name if location else "",
            "room_path": room.path.description if room and room.path else "",
            "room_capacity": room.capacity,
            "field": r.field.name if r.field else "",
            "customer": r.customer.name if r.customer else "",
            "days_info": days_info,
            "workplace" : workplace_name,
            "status" : room.status if room.status else 0
        })
    
    return response  # убираем ограничение [:40]

@router.post("/api/add_resident")
async def add_resident(data: dict = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    try:
        # 1. Месторождение
        res = await db.execute(select(Field).where(Field.name == data["field"]))
        field = res.scalars().first()
        if not field:
            field = Field(name=data["field"])
            db.add(field)

        # 2. Заказчик
        res = await db.execute(select(Customer).where(Customer.name == data["customer"]))
        customer = res.scalars().first()
        if not customer:
            customer = Customer(name=data["customer"])
            db.add(customer)

        # 3. Расположение
        res = await db.execute(select(Location).where(Location.name == data["location"]))
        location = res.scalars().first()
        if not location:
            location = Location(name=data["location"])
            db.add(location)

        # 4. Путь
        res = await db.execute(select(Path).where(Path.description == data["path"]))
        path = res.scalars().first()
        if not path:
            path = Path(description=data["path"])
            db.add(path)

        await db.flush()

        raw_uid = data.get("room_unique_id", "")
        room_unique_id = raw_uid + 'a'
        capacity_val = int(raw_uid) if raw_uid.isdigit() else 0

        res = await db.execute(
            select(Room).where(
                and_(Room.room_number == data['room_number'], Room.room_unique_id == room_unique_id)
            )
        )
        room = res.scalars().first()
        if not room:
            room = Room(
                room_number=data['room_number'],
                field_id=field.id,
                capacity=capacity_val,
                location_id=location.id,
                path_id=path.id,
                room_unique_id=room_unique_id
            )
            db.add(room)
            await db.flush()

        resident = Resident(
            field_id=field.id,
            customer_id=customer.id,
            full_name=data["full_name"],
            check_in=datetime.strptime(data["check_in"], "%Y-%m-%d").date(),
            check_out=datetime.strptime(data["check_out"], "%Y-%m-%d").date(),
            position=data.get("position", ""),
            gender=data.get("gender", ""),
            room_id=room.id,
            shift=data.get("shift", "")
        )
        db.add(resident)
        await db.flush()

        day = ResidentDay(
            resident_id=resident.id,
            room_id=resident.room_id,
            date=resident.check_in,
            extra=resident.check_out,
            customer_id=customer.id,
            # days=days
        )
        db.add(day)
        await db.commit()
        return {"message": "Запись успешно добавлена", "resident_id": resident.id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/update_resident")
async def update_resident(data: dict = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    try:
        res = await db.execute(select(Resident).where(Resident.id == data["id"]))
        resident = res.scalars().first()
        if not resident:
            raise HTTPException(status_code=404, detail="Жилец не найден")

        if "position" in data:
            resident.position = data["position"]
        if "gender" in data:
            resident.gender = data["gender"]
        if "shift" in data:
            resident.shift = data["shift"]
        if "status" in data:
            if resident.room_id:
                # Получаем комнату жильца
                room = await db.execute(select(Room).where(Room.id == resident.room_id))
                room = room.scalars().first()
                if room:
                    room.status = data["status"]

        await db.commit()
        await db.refresh(resident)
        return {"status": "ok"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))