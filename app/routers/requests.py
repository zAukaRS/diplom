from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import date
from ..database import get_db
from ..models import User, Field, Request, Customer, Resident, Room
from ..core.dependencies import get_current_user
from typing import Optional
router = APIRouter(prefix="/api/requests", tags=["requests"])

# Получить свободные места (можно позже реализовать, сейчас просто заглушка)
@router.get("/available")
async def get_available(
    field_id: int,
    check_in: date,
    check_out: date,
    db: AsyncSession = Depends(get_db)
):
    res = await db.get(Field,field_id)
    res = res.scalars().first()
    if not res:
        raise  HTTPException(status_code=400, detail="Нету такого месторождения")
    
    # Здесь можно добавить логику проверки свободных мест, но пока вернём пустой список
    # или список всех комнат месторождения с информацией о занятости.
    # Для MVP можно вернуть заглушку, что место есть.

    return {"room_id": x}


@router.post("/")
async def create_request(
    customer_name : str,
    eol_fio : str,
    resident_name: str,
    position : Optional[str] = None,
    field_name : str,
    check_in: date,
    check_out: date,
    party_1 : str,
    party_2 : str,
    room_num : Optional[str] = None,
    comment: str = "",

    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    customer_name = customer_name.strip()
    eol_fio = eol_fio.strip()
    resident_name = resident_name.strip()
    position = position.strip()
    field_name = field_name.strip()
    room_num = room_num.strip()
    party_1 = party_1.strip()
    party_1 = party_2.strip()
    
    # role
    if current_user.role != 'user':
        raise HTTPException(status_code=400, detail="Вы не работник, у вас другие права.")
    
    res = await db.execute(select(Request_).where(and_(Request.contract_num == contract_num,Request.contract_date == contract_date)))
    res = res.scalars().first()
    if res:
        raise HTTPException(status_code=400, detail="Проверьте корректность введенного контракта")
    
    #field
    res = await db.execute(select(Field).where(Field.name == field_name))
    field = res.scalars().first()
    if not field:
        field = Field(
            name = field_name
        )
        db.add(field)
        await db.commit()
        await db.flush()


    # Проверяем даты
    if check_in > check_out:
        raise HTTPException(400, "Дата заезда не может быть позже даты выезда")
    
    new_req = Request(
        user_id=current_user.id,
        field_id=field_id,
        check_in=check_in,
        check_out=check_out,
        comment=comment,
        status="pending"
    )
    db.add(new_req)
    await db.commit()
    await db.refresh(new_req)
    return {"id": new_req.id, "status": new_req.status}


#просмотр заявок
@router.get("/my")
async def get_my_requests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    result = await db.execute(
        select(Request).where(Request.user_id == current_user.id)
        .order_by(Request.created_at.desc())
    )
    requests = result.scalars().all()
    return [{"id": r.id, "field_id": r.field_id, "check_in": r.check_in,
             "check_out": r.check_out, "comment": r.comment, "status": r.status,
             "admin_comment": r.admin_comment} for r in requests]

# Для админов модерация
@router.get("/field/{field_id}")
async def get_requests_for_field(
    field_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Проверка прав: пользователь либо глобальный админ, либо админ этого поля
    if current_user.role.name != "admin":
        if current_user.field_id != field_id:
            raise HTTPException(403, "Нет доступа к этому месторождению")
    # Проверяем, что поле существует
    field = await db.get(Field, field_id)
    if not field:
        raise HTTPException(404, "Месторождение не найдено")
    result = await db.execute(
        select(Request).where(Request.field_id == field_id)
        .order_by(Request.created_at.desc())
    )
    requests = result.scalars().all()
    return [{"id": r.id, "user_id": r.user_id, "username": r.user.username,
             "check_in": r.check_in, "check_out": r.check_out,  
             "comment": r.comment, "status": r.status,
             "admin_comment": r.admin_comment} for r in requests]



# Обновления заявок
@router.put("/{request_id}")
async def update_request_status(
    request_id: int,
    status: str,
    admin_comment: str = "",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):  
    # Проверка прав
    if current_user.role.name != "admin":
        if current_user.field_id != req.field_id:
            raise HTTPException(403, "Нет прав на изменение этой заявки")
        
    req = await db.get(Request, request_id)
    if not req:
        raise HTTPException(404, "Заявка не найдена")
    
    if status not in ("approved", "rejected"):
        raise HTTPException(400, "Неверный статус")
    req.status = status
    if admin_comment:
        req.admin_comment = admin_comment
    await db.commit()
    return {"message": "Статус обновлён"}



