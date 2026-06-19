from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, or_
from sqlalchemy.orm import selectinload
from datetime import date, timedelta
import os
from typing import Optional, List, Tuple

from app.database import get_db
from app.models import Field, Customer, Request, Resident
from app.core.dependencies import get_current_user
from app.helpers.create_report import create_report, over_time

router = APIRouter()


def merge_intervals(intervals: List[Tuple[date, date]]) -> List[Tuple[date, date]]:
    """Объединяет пересекающиеся интервалы дат."""
    if not intervals:
        return []
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [list(sorted_intervals[0])]
    for start, end in sorted_intervals[1:]:
        if start <= merged[-1][1] + timedelta(days=1):  # разрешаем смежные дни
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [(s, e) for s, e in merged]


def count_days_in_range(intervals: List[Tuple[date, date]], period_start: date, period_end: date) -> int:
    """Считает количество уникальных дней в объединённых интервалах, ограниченных периодом."""
    total = 0
    for start, end in intervals:
        actual_start = max(start, period_start)
        actual_end = min(end, period_end)
        if actual_start <= actual_end:
            total += (actual_end - actual_start).days + 1
    return total


@router.get('/api/get_report')
async def get_report(
    date_in: date,
    date_out: date,
    cost_of_day: Optional[int] = 500,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    if date_in > date_out:
        raise HTTPException(status_code=400, detail="Дата начала не может быть позже даты конца")

    query = (
        select(Request)
        .where(
            Request.status == "approved",
            Request.check_in <= date_out,
            Request.check_out >= date_in
        )
        .options(
            selectinload(Request.field),
            selectinload(Request.customer),
            selectinload(Request.room),
            selectinload(Request.resident)
        )
        .order_by(Request.field_id, Request.customer_id)
    )

    result = await db.execute(query)
    requests = result.scalars().unique().all()

    if not requests:
        raise HTTPException(status_code=404, detail="Нет данных за выбранный период")

    data = []
    for req in requests:
        actual_in = max(req.check_in, date_in)
        actual_out = min(req.check_out, date_out)
        days = (actual_out - actual_in).days + 1

        full_name = req.resident.full_name if req.resident else (req.eol_fio or "—")

        data.append({
            'Месторождение': req.field.name if req.field else "—",
            'Заказчик': req.customer.name if req.customer else "—",
            'ФИО проживающего': full_name,
            'Дата заезда': actual_in,
            'Дата выезда': actual_out,
            'Количество дней': days,
            'Расчет за жилье': days * cost_of_day,
        })

    file_path = create_report(data, f"report_{date_in}_{date_out}.xlsx")
    return FileResponse(file_path, filename=os.path.basename(file_path))


@router.get('/api/get_overtime_report')
async def get_overtime_report(
    check_in: date,
    check_out: date,
    db: AsyncSession = Depends(get_db),
    field_name: Optional[str] = None,
    norm_days: Optional[int] = 15,
    user=Depends(get_current_user)
):
    if check_in > check_out:
        raise HTTPException(status_code=400, detail="Дата начала не может быть позже даты конца")

    # Получаем все утверждённые заявки за период
    query = select(Request).where(
        Request.status == "approved",
        Request.check_in <= check_out,
        Request.check_out >= check_in
    ).options(
        selectinload(Request.field),
        selectinload(Request.customer),
        selectinload(Request.resident)
    )
    if field_name:
        query = query.join(Field, Field.id == Request.field_id).where(Field.name == field_name)

    result = await db.execute(query)
    requests = result.scalars().unique().all()

    if not requests:
        raise HTTPException(status_code=404, detail="Нет данных за выбранный период")

    # Группируем по человеку (resident_id или eol_fio для гостей)
    persons = {}
    for req in requests:
        # Ключ: resident_id или eol_fio
        if req.resident_id:
            key = f"resident_{req.resident_id}"
            name = req.resident.full_name if req.resident else req.eol_fio
        else:
            key = f"guest_{req.eol_fio}"
            name = req.eol_fio
        if not name:
            name = "Неизвестно"

        if key not in persons:
            persons[key] = {
                'name': name,
                'intervals': [],
                'field_name': req.field.name if req.field else "—",
                'customer_name': req.customer.name if req.customer else "—"
            }
        # Обрезаем интервал по периоду отчёта
        start = max(req.check_in, check_in)
        end = min(req.check_out, check_out)
        if start <= end:
            persons[key]['intervals'].append((start, end))

    # Функция объединения интервалов
    def merge_intervals(intervals):
        if not intervals:
            return []
        intervals.sort(key=lambda x: x[0])
        merged = [list(intervals[0])]
        for s, e in intervals[1:]:
            if s <= merged[-1][1] + timedelta(days=1):  # разрешаем смежные
                if e > merged[-1][1]:
                    merged[-1][1] = e
            else:
                merged.append([s, e])
        return [(s, e) for s, e in merged]

    # Собираем отчёт
    data = []
    for key, info in persons.items():
        merged = merge_intervals(info['intervals'])
        total_days = sum((e - s).days + 1 for s, e in merged)
        if total_days >= norm_days:
            actual_in = min(s for s, _ in merged) if merged else check_in
            actual_out = max(e for _, e in merged) if merged else check_out
            data.append({
                'Месторождение': info['field_name'],
                'Заказчик': info['customer_name'],
                'ФИО проживающего': info['name'],
                'Дата заезда': actual_in,
                'Дата выезда': actual_out,
                'Количество дней': total_days,
                'Норма': norm_days,
                'Переработка (дни)': max(0, total_days - norm_days),
                'Переработка в %': round(max(0, total_days - norm_days) / norm_days * 100, 2),
            })

    if not data:
        raise HTTPException(status_code=404, detail="Нет людей с переработкой за выбранный период")

    data.sort(key=lambda x: x['Переработка (дни)'], reverse=True)

    file_path = over_time(
        data,
        f"overtime_{check_in}_{check_out}.xlsx",
        date_from=check_in,
        date_to=check_out,
        norm_days=norm_days,
    )
    return FileResponse(file_path, filename=os.path.basename(file_path))