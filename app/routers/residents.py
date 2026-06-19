from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, union
from sqlalchemy.orm import selectinload
from datetime import datetime, date, timedelta
from typing import Optional
from app.database import get_db
from app.models import Resident, Field, Customer, Location, Path, Room, User, Request, Request_before
from app.core.dependencies import get_current_user
from ..utils import generate_contract_number

router = APIRouter()

def days_in_month(year: int, month: int) -> int:
    if month == 12:
        return 31
    return (date(year, month + 1, 1) - timedelta(days=1)).day

@router.get("/api/residents")
async def get_requests(
    word: Optional[str] = None,
    by_field: Optional[int] = None,
    date_1: Optional[date] = None,
    date_2: Optional[date] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    limit: int = 30,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    current_date_time = datetime.now()
    if month is None:
        month = current_date_time.month
    if year is None:
        year = current_date_time.year

    # Определяем диапазон дат
    if not date_1 and not date_2:
        date_start = date(year, month, 1)
        date_end = date(year, month, days_in_month(year, month))
    elif not date_1 and date_2:
        date_start = date(year, month, current_date_time.day)
        date_end = date_2
    elif date_1 and not date_2:
        date_start = date_1
        date_end = date(year, month + 1, current_date_time.day)
    else:
        date_start = date_1
        date_end = date_2

    # ----- 1. Формальные записи (Request) -----
    query_formal = select(Request).where(
        Request.status == "approved",
        Request.check_in <= date_end,
        Request.check_out >= date_start
    ).options(
        selectinload(Request.field),
        selectinload(Request.customer),
        selectinload(Request.room).selectinload(Room.location),
        selectinload(Request.room).selectinload(Room.path),
        selectinload(Request.resident)
        # selectinload(Request.user).selectinload(User.resident)
    )
    if by_field:
        query_formal = query_formal.where(Request.field_id == by_field)

    # ----- 2. Гостевые записи (Request_before) -----
    query_guest = select(Request_before).where(
        Request_before.status == "approved",
        Request_before.check_in <= date_end,
        Request_before.check_out >= date_start
    ).options(
        selectinload(Request_before.field),
        selectinload(Request_before.room).selectinload(Room.location),
        selectinload(Request_before.room).selectinload(Room.path),
        
    )
    if by_field:
        query_guest = query_guest.where(Request_before.field_id == by_field)

    # Общий поиск по слову – применяем к обоим запросам отдельно
    if word:
        word_lower = word.lower().strip()
        # Формальные
        query_formal = query_formal.outerjoin(Room, Request.room_id == Room.id)\
            .outerjoin(Location, Room.location_id == Location.id)\
            .outerjoin(Customer, Request.customer_id == Customer.id)\
            .outerjoin(User, Request.user_id == User.id)\
            .outerjoin(Resident, User.resident_id == Resident.id)\
            .where(
                or_(
                    Resident.full_name.ilike(f"%{word_lower}%"),
                    Room.room_number.ilike(f"%{word_lower}%"),
                    Location.name.ilike(f"%{word_lower}%"),
                    Customer.name.ilike(f"%{word_lower}%")
                )
            )
        # Гостевые
        query_guest = query_guest.outerjoin(Room, Request_before.room_id == Room.id)\
            .outerjoin(Location, Room.location_id == Location.id)\
            .where(
                or_(
                    Request_before.full_name.ilike(f"%{word_lower}%"),
                    Room.room_number.ilike(f"%{word_lower}%"),
                    Location.name.ilike(f"%{word_lower}%"),
                    Request_before.customer.ilike(f"%{word_lower}%")
                )
            )

    # Выполняем оба запроса
    result_formal = await db.execute(query_formal.limit(limit).offset(offset))
    result_guest = await db.execute(query_guest.limit(limit).offset(offset))
    requests_formal = result_formal.scalars().unique().all()
    requests_guest = result_guest.scalars().unique().all()

    # Формируем единый ответ
    response = []

    # Формальные записи
    for req in requests_formal:
        room = req.room
        location = room.location if room else None
        room_path = room.path.description if room and room.path else ""
        customer = req.customer
        resident = req.resident
        response.append({
            "id": req.id,
            "type": "formal",
            "full_name": resident.full_name if resident else "",
            "position": resident.position if resident else "",
            "gender": resident.gender if resident else "",
            "room_number": room.room_number if room else "",
            "room_location": location.name if location else "",
            "room_path": room_path,
            "room_capacity": room.room_unique_id if room else 0,
            "customer": customer.name if customer else "",
            "check_in": req.check_in,
            "check_out": req.check_out,
            "days": req.days,
            "status": room.status if room and room.status else 0,
        })

    # Гостевые записи
    for req in requests_guest:
        room = req.room
        location = room.location if room else None
        user_1 = await db.get(User, req.user_id)
        if not user_1:
            full_name = user_1.resident.full_name
            postition = user_1.resident.position
            gender = user_1.resident.gender
        else:
            full_name = req.full_name
            postition = req.position
            gender = req.gender
        response.append({
            "id": req.id,
            "type": "guest",
            "full_name": full_name or "",
            "position": postition or "",
            "gender": gender or "",
            "room_number": room.room_number if room else "",
            "room_location": location.name if location else "",
            "room_path": room.path.description if room and room.path else "",
            "room_capacity": room.room_unique_id if room else 0,
            "customer": req.customer or "",
            "check_in": req.check_in,
            "check_out": req.check_out,
            "days": req.days,
            "status": room.status if room and room.status else 0,
        })

    # Простая пагинация – ограничиваем количество
    response = response[offset:offset+limit]
    return response


@router.post("/api/add_resident")
async def add_row(
    data: dict = Body(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    add_in_official = data.get("add_in_official", False)

    if user.role.name not in ("admin", "field_admin"):
        raise HTTPException(403, "Доступ запрещён")

    field = await db.get(Field, data.get("field_id"))
    if not field:
        raise HTTPException(404, "Месторождение не найдено")

    # Преобразование дат
    try:
        check_in = datetime.strptime(data["check_in"], "%Y-%m-%d").date()
        check_out = datetime.strptime(data["check_out"], "%Y-%m-%d").date()
    except (TypeError, ValueError, KeyError):
        raise HTTPException(400, "Неверный формат даты. Ожидается YYYY-MM-DD")

    if check_in > check_out:
        raise HTTPException(400, "Дата заезда не может быть позже даты выезда")

    room = await db.get(Room, data.get("room_id"))
    if not room:
        raise HTTPException(404, "Комната не найдена")

    contract_num = await generate_contract_number(db, field.name)

    # Заказчик
    customer_name = (data.get("customer_name") or "").strip()
    if not customer_name:
        raise HTTPException(400, "Не указан заказчик")
    stmt = select(Customer).where(Customer.name == customer_name)
    customer_obj = (await db.execute(stmt)).scalars().first()
    if not customer_obj:
        customer_obj = Customer(name=customer_name)
        db.add(customer_obj)
        await db.commit()
        await db.refresh(customer_obj)

    full_name = (data.get("full_name") or "").strip()
    if not full_name:
        raise HTTPException(400, "Не указано ФИО")
    position = data.get("position", "")
    gender = data.get("gender", "")

    # Дата заключения договора
    contract_date_raw = data.get("contract_date")
    if contract_date_raw:
        try:
            contract_date = datetime.strptime(contract_date_raw, "%Y-%m-%d").date()
        except (TypeError, ValueError):
            raise HTTPException(400, "Неверный формат даты договора. Ожидается YYYY-MM-DD")
    else:
        contract_date = datetime.now().date()

    if add_in_official:
        # Формальная запись: ищем или создаём Resident
        resident = await db.execute(select(Resident).where(Resident.full_name == full_name))
        resident_obj = resident.scalars().first()
        if not resident_obj:
            resident_obj = Resident(
                full_name=full_name,
                position=position,
                gender=gender,
                birthday=data.get("birthday") or datetime.now().date()
            )
            db.add(resident_obj)
            await db.commit()
            await db.refresh(resident_obj)

        # Находим пользователя, привязанного к этому жителю (или создаём?)
        # Для простоты берём текущего админа, но лучше создать отдельного пользователя.
        # Здесь оставим текущего – ответственность за запись лежит на админе.
        new_request = Request(
            customer_id=customer_obj.id,
            contract_num=contract_num,
            contract_date=contract_date,
            eol_fio=data.get("eol_fio") or full_name,
            user_id=user.id,   # текущий админ — кто оформил запись
            resident_id=resident_obj.id,
            position=position,
            field_id=data["field_id"],
            check_in=check_in,
            check_out=check_out,
            days=(check_out - check_in).days + 1,
            room_id=data["room_id"],
            comment=data.get("comment", ""),
            status="approved",
            admin_comment=data.get("admin_comment") or None,
        )
        db.add(new_request)
        await db.commit()
        await db.refresh(new_request)
        return {"id": new_request.id, "status": new_request.status}

    else:
        # Гостевая запись – сразу в request_before со статусом approved
        new_guest = Request_before(
            customer=customer_name,
            contract_num=contract_num,
            contract_date=contract_date,
            eol_fio=data.get("eol_fio") or full_name,
            user_id=user.id,
            position=position,
            field_id=data["field_id"],
            check_in=check_in,
            check_out=check_out,
            days=(check_out - check_in).days + 1,
            room_id=data["room_id"],
            comment=data.get("comment", ""),
            status="approved",
            admin_comment=data.get("admin_comment") or None,
            full_name=full_name,
            gender=gender,
        )
        db.add(new_guest)
        await db.commit()
        await db.refresh(new_guest)
        return {"id": new_guest.id, "status": new_guest.status}




@router.post("/api/update_resident")
async def update_requests(data: dict = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    try:
        record_type = data.get("type", "formal")

        if record_type == "guest":
            res = await db.execute(select(Request_before).where(Request_before.id == data["id"]))
            record = res.scalars().first()
            if not record:
                raise HTTPException(status_code=404, detail="Жилец не найден")

            if "position" in data:
                record.position = data["position"]

            if "gender" in data:
                record.gender = data["gender"]

            if "status" in data and record.room_id:
                room = await db.execute(select(Room).where(Room.id == record.room_id))
                room = room.scalars().first()
                if room:
                    room.status = data["status"]

            await db.commit()
            await db.refresh(record)
            return {"status": "ok"}

        # record_type == "formal"
        res = await db.execute(select(Request).where(Request.id == data["id"]))
        request = res.scalars().first()
        if not request:
            raise HTTPException(status_code=404, detail="Жилец не найден")

        resident = None
        if request.resident_id:
            resident = await db.get(Resident, request.resident_id)

        if "position" in data:
            request.position = data["position"]
            if resident:
                resident.position = data["position"]

        if "gender" in data and resident:
            resident.gender = data["gender"]

        if "status" in data and request.room_id:
            # Получаем комнату жильца
            room = await db.execute(select(Room).where(Room.id == request.room_id))
            room = room.scalars().first()
            if room:
                room.status = data["status"]

        await db.commit()
        await db.refresh(request)
        return {"status": "ok"}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get("/api/employees/search")
async def search_employees(
    q: str,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if len(q) < 2:
        return []
    pattern = f"%{q}%"
    query = select(Resident).where(Resident.full_name.ilike(pattern)).limit(limit)
    result = await db.execute(query)
    employees = result.scalars().all()
    return [
        {
            "id": e.id,
            "full_name": e.full_name,
            "position": e.position,
            "gender": e.gender,
        }
        for e in employees
    ]


@router.post("/api/convert_resident_type")
async def convert_resident_type(
    data: dict = Body(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Преобразует запись:
    - из гостевой (request_before) в формальную (Request)
    - из формальной (Request) в гостевую (request_before)
    """
    if user.role.name not in ("admin", "field_admin"):
        raise HTTPException(403, "Доступ запрещён")

    record_id = data.get("id")
    target_type = data.get("target_type")  # "formal" или "guest"

    if target_type == "formal":
        # Гостевая -> формальная
        guest = await db.get(Request_before, record_id)
        if not guest:
            raise HTTPException(404, "Гостевая запись не найдена")
        if guest.status != "approved":
            raise HTTPException(400, "Конвертировать можно только одобренные записи")

        # Создаём Resident (или используем существующего)
        resident = await db.execute(select(Resident).where(Resident.full_name == guest.full_name))
        resident_obj = resident.scalars().first()
        if not resident_obj:
            resident_obj = Resident(
                full_name=guest.full_name,
                position=guest.position,
                gender=guest.gender,
                birthday=datetime.now().date()
            )
            db.add(resident_obj)
            await db.flush()

        # Приоритет данных: сначала берём актуальные значения из Resident
        # (могли быть изменены через update_resident), и только если там
        # пусто — используем снимок из гостевой записи (request_before)
        position = resident_obj.position or guest.position
        gender = resident_obj.gender or guest.gender

        # Привязываем Resident к пользователю, чтобы редактирование (update_resident)
        # и обратная конвертация продолжали работать корректно
        guest_user = await db.get(User, guest.user_id)
        if guest_user and not guest_user.resident_id:
            guest_user.resident_id = resident_obj.id

        # Находим заказчика
        stmt = select(Customer).where(Customer.name == guest.customer)
        customer_obj = (await db.execute(stmt)).scalars().first()
        if not customer_obj:
            customer_obj = Customer(name=guest.customer)
            db.add(customer_obj)
            await db.flush()

        # Создаём формальную запись
        new_request = Request(
            customer_id=customer_obj.id,
            contract_num=guest.contract_num,
            contract_date=guest.contract_date,
            eol_fio=guest.eol_fio,
            user_id=guest.user_id,
            resident_id=resident_obj.id,
            position=position,
            field_id=guest.field_id,
            check_in=guest.check_in,
            check_out=guest.check_out,
            days=guest.days,
            room_id=guest.room_id,
            comment=guest.comment,
            status="approved",
            admin_comment=guest.admin_comment,
        )
        db.add(new_request)
        await db.delete(guest)
        await db.commit()
        return {"message": "Запись преобразована в формальную"}

    elif target_type == "guest":
        # Формальная -> гостевая
        formal = await db.get(Request, record_id, options=[selectinload(Request.customer)])
        if not formal:
            raise HTTPException(404, "Формальная запись не найдена")
        if formal.status != "approved":
            raise HTTPException(400, "Конвертировать можно только одобренные записи")

        # Берём данные из связанного Resident (если есть), иначе из самой заявки.
        # Сначала проверяем прямую ссылку Request.resident_id, затем User.resident_id
        # (для старых записей, созданных до появления этого поля)
        resident = None
        if formal.resident_id:
            resident = await db.get(Resident, formal.resident_id)
        else:
            user_obj = await db.get(User, formal.user_id)
            if user_obj and user_obj.resident_id:
                resident = await db.get(Resident, user_obj.resident_id)

        # Приоритет: актуальные данные из Resident, иначе — снимок из заявки
        full_name = (resident.full_name if resident else None) or formal.eol_fio
        gender = (resident.gender if resident else None) or None
        position = (resident.position if resident else None) or formal.position

        # Создаём гостевую запись
        new_guest = Request_before(
            customer=formal.customer.name,
            contract_num=formal.contract_num,
            contract_date=formal.contract_date,
            eol_fio=formal.eol_fio,
            user_id=formal.user_id,
            position=position,
            field_id=formal.field_id,
            check_in=formal.check_in,
            check_out=formal.check_out,
            days=formal.days,
            room_id=formal.room_id,
            comment=formal.comment,
            status="approved",
            admin_comment=formal.admin_comment,
            full_name=full_name,
            gender=gender,
        )
        db.add(new_guest)
        await db.delete(formal)
        await db.commit()
        return {"message": "Запись преобразована в гостевую"}

    raise HTTPException(400, "Неверный target_type")