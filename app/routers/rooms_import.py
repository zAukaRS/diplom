# app/routers/rooms_import.py
import io
import logging
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import Room, Field
from app.core.dependencies import get_current_user
from app.room_importer import apply_to_db_async
from app.simple_room_importer import import_rooms_from_excel

router = APIRouter(prefix="/api/rooms", tags=["rooms_import"])
logger = logging.getLogger(__name__)

@router.get("/check")
async def check_rooms(
    field_id: int,
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    """Проверяет, есть ли комнаты для указанного месторождения."""
    result = await db.execute(select(func.count()).select_from(Room).where(Room.field_id == field_id))
    count = result.scalar() or 0
    return {"count": count}

@router.post("/import")
async def import_rooms(
    file: UploadFile = File(...),
    field_id: int = Form(...),
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Импорт комнат из Excel-файла.
    Сначала проверяет, что для данного field_id нет комнат.
    """
    # Проверяем расширение
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(400, "Файл должен быть формата .xlsx или .xls")

    # Проверяем существование поля
    field = await db.get(Field, field_id)
    if not field:
        raise HTTPException(404, f"Месторождение с id {field_id} не найдено")

    # Проверяем, есть ли уже комнаты
    count_res = await db.execute(select(func.count()).select_from(Room).where(Room.field_id == field_id))
    if count_res.scalar() > 0:
        raise HTTPException(409, "В этом месторождении уже есть комнаты. Импорт невозможен.")

    # Читаем содержимое файла
    content = await file.read()
    if not content:
        raise HTTPException(400, "Файл пуст")

    # Проверяем сигнатуру ZIP (для .xlsx)
    if len(content) < 4 or content[:4] != b'PK\x03\x04':
        # Если это .xls (бинарный), сигнатура другая — пропускаем проверку
        if not file.filename.endswith('.xls'):
            raise HTTPException(400, "Файл не является корректным Excel-файлом (ожидался ZIP-архив для .xlsx). Проверьте, что файл не повреждён и сохранён в формате .xlsx.")

    # Передаём файл как file-like объект
    file_like = io.BytesIO(content)

    # Используем парсер
    try:
        result = import_rooms_from_excel(
            path_or_file=file_like,    # передаём BytesIO
            field_id=field_id,
            sheet_name=None,           # первый лист
            default_path="Основной",
            dry_run=False,
        )
    except Exception as e:
        logger.exception("Ошибка парсинга Excel")
        raise HTTPException(400, f"Ошибка разбора файла: {str(e)}")

    if result.errors:
        # Возвращаем ошибки, но не сохраняем
        return {
            "status": "error",
            "errors": result.errors,
            "summary": result.summary()
        }

    # Сохраняем в БД асинхронно
    try:
        stats = await apply_to_db_async(result, db, field_id, skip_existing=True)
        return {
            "status": "success",
            "locations": stats["locations"],
            "paths": stats["paths"],
            "rooms": stats["rooms"],
            "skipped": stats["skipped"],
            "errors": result.errors,
        }
    except Exception as e:
        await db.rollback()
        logger.exception("Ошибка сохранения в БД")
        raise HTTPException(500, f"Ошибка сохранения: {str(e)}")