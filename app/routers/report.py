from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_,func,case, nulls_last,desc
from sqlalchemy.orm import selectinload
from datetime import date
import os
from typing import Optional
from app.database import get_db
from app.models import Resident, Field, Customer,ResidentDay
# from app.core.dependencies import get_current_user
from app.helpers.create_report import create_report,over_time
router = APIRouter()

@router.get('/api/get_report')
async def get_report(
    date_in: date,
    date_out: date,
    db: AsyncSession = Depends(get_db),
    # user=Depends(get_current_user)
):
    res = await db.execute(
        select(Resident)
        .join(Field, Field.id == Resident.field_id)
        .join(Customer, Customer.id == Resident.customer_id)
        .join(ResidentDay, ResidentDay.resident_id == Resident.id)
        .where(and_(Resident.check_in <= date_out, Resident.check_out >= date_in))
        .order_by(Field.name, Customer.name)
        .options(selectinload(Resident.field), 
                 selectinload(Resident.customer),
                 selectinload(Resident.resident_days))
        )
    residents = res.scalars().unique().all()
    if not residents:
        raise HTTPException(status_code=404, detail="Нет данных за выбранный период")
    
    data = []
    for r in residents:
        actual_in = r.check_in if r.check_in >= date_in else date_in
        actual_out = r.check_out if r.check_out and r.check_out <= date_out else date_out
        
        data.append({
            'Месторождение': r.field.name,
            'Заказчик': r.customer.name,
            'ФИО проживающего': r.full_name,
            'Дата заезда': actual_in,
            'Дата выезда': actual_out,
            'Количество дней': r.resident_days[0].days
        })
    file_path = create_report(data, f"report_{date_in}_{date_out}.xlsx")
    return FileResponse(file_path, filename=os.path.basename(file_path))

@router.get('/api/get_overtime_report')
async def get_overtime_report(
    date_from: date,
    date_to: date,
    db: AsyncSession = Depends(get_db),
    field_name: Optional[str] = None,
    norm_days: int = 15,
):
    """
    Отчёт по переработке: жильцы у которых суммарно дней >= norm_days за период.
    Сортировка по убыванию дней.
    """
    
    date_end = func.least(ResidentDay.extra, date_to)
    date_start = func.greatest(ResidentDay.date, date_from)
    # Вычитание дат даёт целое число дней. Прибавляем 1, чтобы включить оба конца диапазона.
    overlap_days = (date_end - date_start) + 1
 
    days_in_period = func.sum(
        case(
            (
                and_(ResidentDay.date <= date_to, ResidentDay.extra >= date_from),
                overlap_days
            ),
            else_=0
        )
    ).label("days_total")
 
    query = (
        select(
            Field.name.label("field_name"),
            Resident.full_name.label("full_name"),
            Customer.name.label("customer_name"),
            days_in_period,
        )
        .select_from(ResidentDay)
        .join(Resident, Resident.id == ResidentDay.resident_id)
        .join(Field, Field.id == Resident.field_id)
        .join(Customer, Customer.id == ResidentDay.customer_id)
        .where(
            ResidentDay.date <= date_to,
            ResidentDay.extra >= date_from,
        )
        .group_by(
            Field.id,
            Field.name,
            Resident.id,
            Resident.full_name,
            Customer.id,
            Customer.name,
        )
        .having(days_in_period >= norm_days)
        .order_by(desc(days_in_period), Field.name, Customer.name, Resident.full_name)
    )
 
    if field_name:
        query = query.where(Field.name == field_name)
 
    res = await db.execute(query)
    rows = res.all()
 
    if not rows:
        raise HTTPException(status_code=404, detail="Нет данных за выбранный период")
 
    data = [
        {
            'Месторождение': row.field_name,
            'Заказчик': row.customer_name,
            'ФИО проживающего': row.full_name,
            'Количество дней': int(row.days_total or 0),
        }
        for row in rows
    ]
 
    file_path = over_time(
        data,
        f"overtime_{date_from}_{date_to}.xlsx",
        date_from=date_from,
        date_to=date_to,
        norm_days=norm_days,
    )
    return FileResponse(file_path, filename=os.path.basename(file_path))