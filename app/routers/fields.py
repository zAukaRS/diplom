from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Field
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/api/fields")
async def get_fields(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(Field))
    fields = result.scalars().all()
    return [{"id": f.id, "name": f.name} for f in fields]