from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import date
from app.database import get_db
from app.models import ResidentDay, Resident
from app.core.dependencies import get_current_user

router = APIRouter()

@router.post("/api/update_day")
async def update_day(data: dict = Body(...), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    try:
        resident_id = int(data["resident_id"])
        day = int(data["day"])
        month = int(data["month"])
        year = int(data["year"])
        customer_id = data.get("customer_id")
        if customer_id is not None:
            customer_id = int(customer_id)

        target_date = date(year, month, day)

        res = await db.execute(
            select(ResidentDay).where(
                and_(ResidentDay.resident_id == resident_id, ResidentDay.date == target_date)
            )
        )
        rd = res.scalars().first()

        if rd:
            rd.customer_id = customer_id
        else:
            res_r = await db.execute(select(Resident).where(Resident.id == resident_id))
            resident = res_r.scalars().first()
            if not resident:
                raise HTTPException(404, f"Проживающий {resident_id} не найден")
            rd = ResidentDay(
                resident_id=resident_id,
                room_id=resident.room_id,
                date=target_date,
                extra=resident.check_out,
                customer_id=customer_id
            )
            db.add(rd)

        await db.commit()
        return {"status": "ok"}
    except HTTPException as he:
        raise he
    except Exception as e:
        await db.rollback()
        raise HTTPException(400, detail=str(e))