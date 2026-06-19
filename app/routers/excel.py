import io
import logging
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.request_import import import_requests_from_excel

logger = logging.getLogger("excel_upload")

router = APIRouter()

@router.post("/api/upload_excel")
async def upload_excel(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename.endswith((".xlsx", ".xls")):
        logger.warning("UPLOAD_REJECTED: неверный формат файла '%s', user_id=%s", file.filename, current_user.id)
        return JSONResponse({"error": "Неверный формат файла"}, status_code=400)

    try:
        contents = await file.read()
        logger.info(
            "UPLOAD_START: файл='%s' (%s байт), user_id=%s",
            file.filename, len(contents), current_user.id,
        )
        # Включаем подробный вывод в консоль
        stats = await import_requests_from_excel(
            db,
            io.BytesIO(contents),
            created_by_user_id=current_user.id,
            verbose=True,   # <-- здесь включаем логирование
        )
    except Exception as e:
        await db.rollback()
        # также печатаем ошибку в консоль
        logger.error("UPLOAD_FAILED: критическая ошибка при импорте файла '%s': %s", file.filename, e, exc_info=True)
        print(f"❌ Критическая ошибка при импорте: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

    total = stats.approved_formal + stats.approved_guest
    message = f"Одобрено и заселено: {total}"
    if stats.rejected_no_room:
        message += f", отказано из-за нехватки мест: {stats.rejected_no_room}"
    if stats.duplicates_skipped:
        message += f", пропущено как дубликаты: {stats.duplicates_skipped}"
    if stats.rows_skipped:
        message += f", пропущено с ошибкой: {stats.rows_skipped}"

    logger.info(
        "UPLOAD_DONE: файл='%s', user_id=%s, итог: %s",
        file.filename, current_user.id, message,
    )

    return {
        "message": message,
        "approved_formal": stats.approved_formal,
        "approved_guest": stats.approved_guest,
        "rejected_no_room": stats.rejected_no_room,
        "duplicates_skipped": stats.duplicates_skipped,
        "rows_skipped": stats.rows_skipped,
        "customers_created": stats.customers_created,
        "fields_created": stats.fields_created,
        "residents_created": stats.residents_created,
        "days_mismatch_warnings": stats.days_mismatch_warnings[:20],
        "resident_overlap_warnings": stats.resident_overlap_warnings[:20],
        "errors": stats.errors[:20],
    }