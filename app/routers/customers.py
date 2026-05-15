from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Customer
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/api/customers")
async def get_customers(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    res = await db.execute(select(Customer))
    customers = res.scalars().all()
    return [{"id": c.id, "name": c.name} for c in customers]