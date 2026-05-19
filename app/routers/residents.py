
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from datetime import datetime
from typing import Optional
from app.database import get_db
from app.models import Resident, Field, Customer, Location, Path, Room, ResidentDay
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/api/residents")
async def get_residents(
    word: Optional[str] = None,
    by_field: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    query = select(Resident).options(
        selectinload(Resident.field),
        selectinload(Resident.customer),
        selectinload(Resident.room).selectinload(Room.location),
        selectinload(Resident.room).selectinload(Room.path),
        selectinload(Resident.resident_days)
    )

    if by_field and by_field.strip():
        try:
            field_id = int(by_field)
            query = query.where(Resident.field_id == field_id)
        except ValueError:
            pass

    if word:
        word_lower = word.lower().strip()
        query = query.outerjoin(Room).outerjoin(Location).outerjoin(Customer).where(
            or_(
                Resident.full_name.ilike(f"%{word_lower}%"),
                Resident.position.ilike(f"%{word_lower}%"),
                Room.room_number.ilike(f"%{word_lower}%"),
                Location.name.ilike(f"%{word_lower}%"),
                Customer.name.ilike(f"%{word_lower}%")
            )
        )

    result = await db.execute(query)
    residents = result.scalars().unique().all()
    if not residents:
        return []

    response = []
    for r in residents:
        room = r.room
        location = room.location if room else None
        days_info = {rd.date.day: rd.customer_id for rd in r.resident_days}
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
    return response[:10]

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

        await db.commit()
        await db.refresh(resident)
        return {"status": "ok"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))