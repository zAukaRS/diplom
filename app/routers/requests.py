from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from datetime import date,datetime
from ..database import get_db
from ..models import User, Field, Request, Customer, Resident, Room,Request_before
from ..core.dependencies import get_current_user
from ..utils import generate_contract_number
from typing import Optional

router = APIRouter(prefix="/api/requests", tags=["requests"])
from pydantic import BaseModel

class RequestCreate(BaseModel):
    customer: str
    contract_date: date
    eol_fio: str          
    position: str
    field_id: int
    check_in: date
    check_out: date
    room_id: int
    comment: Optional[str] = ""
    contract_num: str
    full_name: str        
    gender: Optional[str] = None  


# Получить свободные места с учётом вместимости комнат.
#
# Логика: уникальное "место" определяется парой (room_number, room_unique_id).
# Несколько строк Room с одинаковым room_number, но разными room_unique_id —
# это варианты одной и той же физической комнаты (например, 101/2a и 101/2b).
# Общая вместимость группы room_number = сумма capacity всех вариантов.
# Занятость группы = сумма заявок (Request/Request_before) на пересекающийся
# период по ЛЮБОЙ из комнат этой группы.
# free_places для группы = суммарная вместимость - суммарная занятость.
# Для бронирования возвращаем конкретный room_id одного из вариантов группы,
# у которого ещё есть свободное место (его собственная capacity > его occupied).
async def compute_available_rooms(
    db: AsyncSession,
    field_id: int,
    check_in: date,
    check_out: date,
):
    """Основная логика подсчёта свободных мест — вынесена из эндпоинта /available,
    чтобы её же использовал импорт заявок из Excel (см. app/request_import.py).
    Предполагается, что field_id существует и check_in <= check_out — это
    проверяет вызывающий код (см. эндпоинт ниже)."""

    # Все комнаты месторождения, не находящиеся на ремонте (status == 1 — ремонт)
    rooms_query = select(Room).where(
        Room.field_id == field_id,
        or_(Room.status == 0, Room.status.is_(None))
    )
    rooms = (await db.execute(rooms_query)).scalars().all()
    if not rooms:
        return []

    room_ids = [r.id for r in rooms]

    # Считаем занятость каждой конкретной комнаты (room_id) на пересекающийся период
    # (только активные заявки — approved и pending; rejected не блокируют место)
    busy_formal = await db.execute(
        select(Request.room_id, func.count(Request.id))
        .where(
            Request.room_id.in_(room_ids),
            Request.status.in_(("approved", "pending")),
            Request.check_in <= check_out,
            Request.check_out >= check_in,
        )
        .group_by(Request.room_id)
    )
    busy_guest = await db.execute(
        select(Request_before.room_id, func.count(Request_before.id))
        .where(
            Request_before.room_id.in_(room_ids),
            Request_before.status.in_(("approved", "pending")),
            Request_before.check_in <= check_out,
            Request_before.check_out >= check_in,
        )
        .group_by(Request_before.room_id)
    )

    occupancy = {}
    for room_id, count in busy_formal.all():
        occupancy[room_id] = occupancy.get(room_id, 0) + count
    for room_id, count in busy_guest.all():
        occupancy[room_id] = occupancy.get(room_id, 0) + count

    # Группируем комнаты по room_number — это физическая комната,
    # а room_unique_id различает варианты внутри неё
    groups = {}
    for r in rooms:
        groups.setdefault(r.room_number, []).append(r)

    available_rooms = []
    for room_number, variants in groups.items():
        total_capacity = sum((v.capacity or 0) for v in variants)
        total_occupied = sum(occupancy.get(v.id, 0) for v in variants)
        group_free = total_capacity - total_occupied
        if group_free <= 0:
            continue

        # Среди вариантов группы ищем те, у которых ещё есть собственное
        # свободное место — туда можно реально заселить
        variant_options = []
        for v in variants:
            v_occupied = occupancy.get(v.id, 0)
            v_free = (v.capacity or 0) - v_occupied
            if v_free > 0:
                variant_options.append({
                    "id": v.id,
                    "room_unique_id": v.room_unique_id,
                    "capacity": v.capacity,
                    "occupied": v_occupied,
                    "free_places": v_free,
                })

        if not variant_options:
            # Теоретически не должно происходить, если group_free > 0,
            # но на случай рассинхронизации данных - пропускаем группу
            continue

        # Берём первый вариант с местом как room_id для бронирования по умолчанию
        default_variant = variant_options[0]
        any_room = variants[0]

        available_rooms.append({
            "id": default_variant["id"],
            "room_number": room_number,
            "room_unique_id": default_variant["room_unique_id"],
            "location_id": any_room.location_id,
            "capacity": total_capacity,
            "occupied": total_occupied,
            "free_places": group_free,
            "variants": variant_options,
        })
    print(f"Occupancy for field {field_id} on {check_in}–{check_out}: {occupancy}")
    return available_rooms


@router.get("/available")
async def get_available(
    field_id: int,
    check_in: date,
    check_out: date,
    db: AsyncSession = Depends(get_db)
):
    
    res = await db.get(Field, field_id)
    if not res:
        raise HTTPException(status_code=400, detail="Нету такого месторождения")
    if check_in > check_out:
        raise HTTPException(400, "Дата заезда не может быть позже даты выезда")

    return await compute_available_rooms(db, field_id, check_in, check_out)



@router.post("/")
async def create_request(
    data: RequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Проверка поля
    field = await db.get(Field, data.field_id)
    if not field:
        raise HTTPException(404, "Месторождение не найдено")

    # 2. Проверка комнаты и принадлежности полю
    room = await db.get(Room, data.room_id)
    if not room:
        raise HTTPException(404, "Комната не найдена")
    if room.field_id != data.field_id:
        raise HTTPException(400, "Room does not belong to the specified field")

    # 3. Проверка дат
    if data.check_in > data.check_out:
        raise HTTPException(400, "Дата заезда не может быть позже даты выезда")

    # 4. Проверка свободных мест
    available = await compute_available_rooms(db, data.field_id, data.check_in, data.check_out)
    if not any(r["id"] == data.room_id for r in available):
        # room_id может быть не в списке, если мест нет
        # можно проверить точнее: есть ли комната с id == data.room_id и free_places > 0
        room_available = False
        for group in available:
            if group["id"] == data.room_id or any(v["id"] == data.room_id for v in group.get("variants", [])):
                # проверить, что в этом варианте есть свободные места
                for variant in group.get("variants", []):
                    if variant["id"] == data.room_id and variant["free_places"] > 0:
                        room_available = True
                        break
                if not room_available:
                    # если группа имеет свободные места, но не этот конкретный вариант,
                    # можно разрешить или предложить другой вариант.
                    # Пока просто ошибка.
                    raise HTTPException(400, "В выбранной комнате нет свободных мест на указанный период")
                break
        if not room_available:
            raise HTTPException(400, "В выбранной комнате нет свободных мест на указанный период")

    # 5. Получение/создание заказчика
    customer_stmt = select(Customer).where(Customer.name == data.customer)
    customer = (await db.execute(customer_stmt)).scalars().first()
    if not customer:
        customer = Customer(name=data.customer)
        db.add(customer)
        await db.flush()

    # 6. Получение/создание жильца (Resident)
    resident_stmt = select(Resident).where(Resident.full_name == data.full_name)
    resident = (await db.execute(resident_stmt)).scalars().first()
    if not resident:
        resident = Resident(
            full_name=data.full_name,
            position=data.position,
            gender=data.gender,
            birthday=None  # или можно передать из запроса
        )
        db.add(resident)
        await db.flush()

    # 7. Генерация номера договора
    contract_num = await generate_contract_number(db, field.name)

    # 8. Создание Request
    new_request = Request(
        customer_id=customer.id,
        contract_num=contract_num,
        contract_date=data.contract_date,
        eol_fio=data.eol_fio,
        user_id=current_user.id,
        resident_id=resident.id,
        position=data.position,
        field_id=data.field_id,
        check_in=data.check_in,
        check_out=data.check_out,
        days=(data.check_out - data.check_in).days + 1,
        room_id=data.room_id,
        comment=data.comment,
        status="approved",    # сразу одобрена
        admin_comment=None,
    )
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)

    return {"id": new_request.id, "status": new_request.status}

#просмотр заявок
@router.get("/my")
async def get_my_requests(
    req_type: str = "drafts",  # принимаем "drafts" или "approved"
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    if req_type == "drafts":
        result = await db.execute(
            select(Request_before)
            .where(Request_before.user_id == current_user.id)
            .order_by(Request_before.created_at.desc())
        )
    else:
        result = await db.execute(
            select(Request)
            .where(Request.user_id == current_user.id)
            .order_by(Request.created_at.desc())
        )
    requests = result.scalars().all()
   
    return requests

# Для админов модерация

# СХЕМА ДЛЯ ОБНОВЛЕНИЯ ЧЕРНОВИКА 
class RequestBeforeUpdate(BaseModel):
    customer: Optional[str] = None
    contract_num: Optional[str] = None
    contract_date: Optional[date] = None
    eol_fio: Optional[str] = None
    position: Optional[str] = None
    field_id: Optional[int] = None
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    days: Optional[int] = None
    room_id: Optional[int] = None
    comment: Optional[str] = None
    status: Optional[str] = None        
    admin_comment: Optional[str] = None


@router.patch("/{request_id}")
async def update_request_before(
    request_id: int,
    update_data: RequestBeforeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Обновление полей черновика заявки. Изменяются только переданные поля."""
        
    if "status" in update_data.model_dump(exclude_unset=True):
        raise HTTPException(403, "Изменение статуса через этот эндпоинт запрещено. Используйте /approve или /reject.")
    req = await db.get(Request_before, request_id)
    if not req:
        raise HTTPException(404, "Черновик не найден")

    # 2. Проверка прав: admin или field_admin, и поле совпадает
    is_admin = current_user.role.name == "admin"
    is_field_admin = current_user.role.name == "field_admin"
    if not (is_admin or (is_field_admin and current_user.field_id == req.field_id)):
        raise HTTPException(403, "Нет прав на редактирование этой заявки")



    
    if req.status == "approved":
        raise HTTPException(409, "Одобренную заявку нельзя редактировать. Создайте новую.")

    
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(req, field, value)
    await db.commit()
    return {"message": "Черновик обновлён"}

# ========== ОДОБРЕНИЕ ЗАЯВКИ ==========
@router.post("/{request_id}/approve")
async def approve_request(
    request_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Одобрение черновика и перенос данных в основную таблицу Request."""
    # 1. Находим черновик
    req = await db.get(Request_before, request_id)
    if not req:
        raise HTTPException(404, "Черновик не найден")

    # 2. Проверка прав (аналогично)
    is_admin = current_user.role.name == "admin"
    is_field_admin = current_user.role.name == "field_admin"
    if not (is_admin or (is_field_admin and current_user.field_id == req.field_id)):
        raise HTTPException(403, "Нет прав на одобрение этой заявки")

    # 3. Если уже одобрена – ошибка
    if req.status == "approved":
        raise HTTPException(409, "Заявка уже была одобрена")
        
    if req.status == "rejected":
        raise HTTPException(409, "Заявка отклонена")
    # 4. Преобразование строки customer → customer_id
    if req.customer:
        stmt = select(Customer).where(Customer.name == req.customer)
        customer = (await db.execute(stmt)).scalars().first()
        if not customer:
            # Можно создать нового заказчика автоматически
            customer = Customer(name=req.customer)
            db.add(customer)
            await db.flush()
        customer_id = customer.id
    
    field = await db.get(Field,req.field_id)
    if not field:
        raise HTTPException(404, "Месторождение не найдено")
    
    contract_num = await generate_contract_number(db, field.name)
    
    # 5. Создаём запись в основной таблице Request
       
    new_request = Request(
        customer_id=customer_id,
        contract_num=contract_num,
        contract_date=req.contract_date,
        eol_fio=req.eol_fio,
        user_id=req.user_id,
        position=req.position,
        field_id=req.field_id,
        check_in=req.check_in,
        check_out=req.check_out,
        days=req.days,
        room_id=req.room_id,
        comment=req.comment,
        status="approved",
        admin_comment=req.admin_comment,
    )
    db.add(new_request)

    # 6. Удаляем черновик, чтобы избежать дублирования
    await db.delete(req)

    await db.commit()
    return {"message": "Заявка одобрена и перенесена в основную таблицу"}


@router.get("/pending")
async def get_pending_requests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Возвращает все черновики со статусом 'pending' (не одобренные) для текущего администратора."""
    is_admin = current_user.role.name == "admin"
    is_field_admin = current_user.role.name == "field_admin"

    query = select(Request_before).where(Request_before.status == "pending")
    if is_field_admin and not is_admin:
        # Показываем только заявки своего поля
        query = query.where(Request_before.field_id == current_user.field_id)
    # Для admin – все заявки

    result = await db.execute(query)
    requests = result.scalars().all()
    return requests


@router.get("/{request_id}")
async def get_request_before(
    request_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    req = await db.get(Request_before, request_id)
    if not req:
        raise HTTPException(404, "Не найдено")

    is_admin = current_user.role.name == "admin"
    is_field_admin = current_user.role.name == "field_admin"
    if not (is_admin or (is_field_admin and current_user.field_id == req.field_id)):
        raise HTTPException(403, "Нет доступа")
    return req

@router.post("/{request_id}/reject")
async def reject_request(
    request_id: int,
    admin_comment: str = "",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    req = await db.get(Request_before, request_id)
    if not req:
        raise HTTPException(404, "Черновик не найден")
    is_admin = current_user.role.name == "admin"
    is_field_admin = current_user.role.name == "field_admin"
    if not (is_admin or (is_field_admin and current_user.field_id == req.field_id)):
        raise HTTPException(403, "Нет прав")
    if req.status in ("approved", "rejected"):
        raise HTTPException(409, f"Заявка уже {req.status}")
    req.status = "rejected"
    if admin_comment:
        req.admin_comment = admin_comment
    await db.commit()
    return {"message": "Заявка отклонена"}


@router.delete("/{request_id}")
async def delete_request_before(
    request_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Удаление черновика (только для владельца или админа)"""
    req = await db.get(Request_before, request_id)
    if not req:
        raise HTTPException(404, "Черновик не найден")
    is_admin = current_user.role.name in ("admin", "field_admin")
    if not (is_admin or req.user_id == current_user.id):
        raise HTTPException(403, "Нет прав на удаление")
    if req.status == "approved":
        raise HTTPException(409, "Нельзя удалить одобренную заявку")
    await db.delete(req)
    await db.commit()
    return {"message": "Черновик удалён"}