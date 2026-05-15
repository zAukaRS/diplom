from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from datetime import date
import os
from app.database import get_db
from app.models import Resident, Field, Customer
from app.core.dependencies import get_current_user
from app.helpers.create_report import create_report
router = APIRouter()

@router.get('/api/get_report')
async def get_report(
    date_in: date,
    date_out: date,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    res = await db.execute(
        select(Resident)
        .join(Field, Field.id == Resident.field_id)
        .join(Customer, Customer.id == Resident.customer_id)
        .where(and_(Resident.check_in <= date_out, Resident.check_out >= date_in))
        .order_by(Field.name, Customer.name)
        .options(selectinload(Resident.field), selectinload(Resident.customer))
    )
    residents = res.scalars().unique().all()
    if not residents:
        raise HTTPException(status_code=404, detail="Нет данных за выбранный период")

    data = []
    for r in residents:
        actual_in = r.check_in if r.check_in >= date_in else date_in
        actual_out = r.check_out if r.check_out and r.check_out <= date_out else date_out
        days = (actual_out - actual_in).days + 1
        data.append({
            'Месторождение': r.field.name,
            'Заказчик': r.customer.name,
            'ФИО проживающего': r.full_name,
            'Дата заезда': actual_in,
            'Дата выезда': actual_out,
            'Количество дней': days
        })
    file_path = create_report(data, f"report_{date_in}_{date_out}.xlsx")
    return FileResponse(file_path, filename=os.path.basename(file_path))