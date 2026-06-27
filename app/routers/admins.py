from fastapi import APIRouter, Depends, Request, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models import User, Role, Field
from app.core.security import get_password_hash
from app.core.dependencies import get_current_user
from app.utils import get_admin_role_id
from app.routers.pages import admin_only
router = APIRouter()



@router.get("/api/get_admins")
async def get_admins(db: AsyncSession = Depends(get_db), user: User = Depends(admin_only)):
    res = await db.execute(
        select(User)
        .join(Role, User.role_id == Role.id)
        .where(Role.name == 'admin')
        .options(selectinload(User.field))
    )
    admins = res.scalars().unique().all()
    result = []
    for u in admins:
        field_name = u.field.name if hasattr(u, "field") and u.field else ""
        result.append({"id": u.id, "username": u.username, "field": field_name})
    return result

@router.post("/api/create_admin")
async def create_admin(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(admin_only)
):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    field_id = data.get("field_id")
    if not username or not password:
        return JSONResponse({"error": "Все поля обязательны"}, status_code=400)

    res = await db.execute(select(User).where(User.username == username))
    if res.scalars().first():
        return JSONResponse({"error": "Логин уже существует"}, status_code=400)

    admin_role_id = await get_admin_role_id(db)
    hashed_password = get_password_hash(password)
    new_admin = User(
        username=username,
        password=hashed_password,
        role_id=1,
        field_id=field_id if field_id else None,
    )
    db.add(new_admin)
    await db.commit()
    await db.refresh(new_admin)
    return {"message": f"Админ {username} создан!"}

@router.put("/api/update_admin_inline/{admin_id}")
async def update_admin_inline(
    admin_id: int,
    data: dict = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    try:
        res = await db.execute(select(User).where(User.id == admin_id))
        admin = res.scalars().first()
        if not admin:
            return JSONResponse({"error": "Админ не найден"}, status_code=404)
        if data.get("username"):
            admin.username = data["username"]
        if data.get("password"):
            admin.password = get_password_hash(data["password"])
        if data.get("field_id"):
            admin.field_id = data["field_id"]
        await db.commit()
        return {"message": "Обновлено"}
    except Exception as e:
        await db.rollback()
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)

@router.delete("/api/delete_admin/{admin_id}")
async def delete_admin(
    admin_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    try:
        res = await db.execute(select(User).where(User.id == admin_id))
        admin = res.scalars().first()
        if not admin:
            return JSONResponse({"error": "Админ не найден"}, status_code=404)
        await db.delete(admin)
        await db.commit()
        return {"message": "Админ удален"}
    except Exception as e:
        await db.rollback()
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)
    

  
from app.models import Field

@router.post("/api/fields/create")
async def create_field(
    data: dict = Body(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(admin_only)  
):
    field_name = data.get("name")
    if not field_name:
        raise HTTPException(status_code=400, detail="Название обязательно")
    

    existing = await db.execute(select(Field).where(Field.name == field_name))
    if existing.scalars().first():
        return {"id": existing.scalars().first().id, "name": field_name}
    
    new_field = Field(name=field_name)
    db.add(new_field)
    await db.commit()
    await db.refresh(new_field)
    return {"id": new_field.id, "name": new_field.name}





from app.models import Request_before, Request, Resident, Customer
from sqlalchemy.orm import selectinload

@router.get("/api/requests/all")
async def get_all_requests(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(admin_only)
):
    """
    Возвращает все заявки из Request_before (pending/rejected/approved)
    и Request (approved), отсортированные по дате создания (новые первые).
    """

    # ---- Request_before ------------------------------------------------
    rb_res = await db.execute(
        select(Request_before)
        .options(selectinload(Request_before.field))
        .order_by(Request_before.created_at.desc())
        .limit(500)
    )
    rb_rows = rb_res.scalars().unique().all()

    rb_list = []
    for r in rb_rows:
        rb_list.append({
            "source": "request_before",
            "id": r.id,
            "status": r.status,
            "user_id": r.user_id,
            "field_id": r.field_id,
            "field_name": r.field.name if r.field else "",
            "check_in": str(r.check_in) if r.check_in else "",
            "check_out": str(r.check_out) if r.check_out else "",
            "room_id": r.room_id,
            "customer": r.customer or "",
            "contract_num": r.contract_num or "",
            "contract_date": str(r.contract_date) if r.contract_date else "",
            "eol_fio": r.eol_fio or "",
            "position": r.position or "",
            "full_name": r.full_name or "",
            "comment": r.comment or "",
            "admin_comment": r.admin_comment or "",
            "created_at": str(r.created_at) if r.created_at else "",
        })

    # ---- Request (approved) --------------------------------------------
    rq_res = await db.execute(
        select(Request)
        .options(
            selectinload(Request.field),
            selectinload(Request.customer),
            selectinload(Request.resident),
        )
        .order_by(Request.created_at.desc())
        .limit(500)
    )
    rq_rows = rq_res.scalars().unique().all()

    rq_list = []
    for r in rq_rows:
        rq_list.append({
            "source": "request",
            "id": r.id,
            "status": r.status,
            "user_id": r.user_id,
            "field_id": r.field_id,
            "field_name": r.field.name if r.field else "",
            "check_in": str(r.check_in) if r.check_in else "",
            "check_out": str(r.check_out) if r.check_out else "",
            "room_id": r.room_id,
            "customer": r.customer.name if r.customer else "",
            "contract_num": r.contract_num or "",
            "contract_date": str(r.contract_date) if r.contract_date else "",
            "eol_fio": r.eol_fio or "",
            "position": r.position or "",
            "full_name": r.resident.full_name if r.resident else "",
            "comment": r.comment or "",
            "admin_comment": r.admin_comment or "",
            "created_at": str(r.created_at) if r.created_at else "",
        })

    # Объединяем и сортируем по created_at (строки ISO, лексикографически)
    all_requests = rb_list + rq_list
    all_requests.sort(key=lambda x: x["created_at"], reverse=True)

    return all_requests


@router.post("/api/requests/{request_id}/reject_admin")
async def reject_request_admin(
    request_id: int,
    source: str = "request_before",   # query param: request_before | request
    data: dict = Body(default={}),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(admin_only),
):
    """
    Отклоняет заявку из любой таблицы (указывается через ?source=).
    """
    admin_comment = data.get("admin_comment", "")

    if source == "request":
        res = await db.execute(select(Request).where(Request.id == request_id))
        req = res.scalars().first()
    else:
        res = await db.execute(select(Request_before).where(Request_before.id == request_id))
        req = res.scalars().first()

    if not req:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    req.status = "rejected"
    if admin_comment:
        req.admin_comment = admin_comment

    await db.commit()
    return {"message": "Заявка отклонена"}