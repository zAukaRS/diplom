from __future__ import annotations
from fastapi import HTTPException
import logging
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Dict, List, Union

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Customer, Field, Request, Request_before, Resident, Room
from app.excel_parser import ParsedRequestRow, parse_workbook
from app.utils import generate_contract_number
from app.routers.requests import compute_available_rooms

logger = logging.getLogger("excel_import")

DEFAULT_GPNV_CUSTOMER_NAME = "ООО «Газпромнефть-Восток»"
NO_ROOM_COMMENT = "Нет свободных мест на запрошенный период"
DUPLICATE_COMMENT = "Пропущено: дубликат уже существующей заявки"

# Статусы заявок, которые считаем активными и учитываем при поиске
ACTIVE_REQUEST_STATUSES = ("approved", "pending")


@dataclass
class ImportStats:
    approved_formal: int = 0
    approved_guest: int = 0
    rejected_no_room: int = 0
    duplicates_skipped: int = 0         
    rows_skipped: int = 0
    expired_skipped: int = 0             # заявки с датой в прошлом
    customers_created: list[str] = field(default_factory=list)
    fields_created: list[str] = field(default_factory=list)
    residents_created: list[str] = field(default_factory=list)
    resident_overlap_warnings: list[str] = field(default_factory=list)
    days_mismatch_warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

async def _delete_requests(db, requests):
    for r in requests:
        await db.delete(r)
    await db.flush()
# ---------------------------------------------------------------------------
# Нормализация
# ---------------------------------------------------------------------------
def normalize_field_name(name: str) -> str:
    if not name:
        return ""
    name = str(name)
    name = name.replace("\xa0", " ")
    name = "".join(" " if unicodedata.category(ch) == "Zs" else ch for ch in name)
    name = name.lower()
    name = name.replace("месторождение", "").replace("месторожд.", "").replace("месторожд", "")
    name = name.replace("гпн", "").replace('"', "").replace("«", "").replace("»", "")
    name = re.sub(r"[.,]+", "", name)
    name = re.sub(r"[\r\n\t]+", " ", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip()


def normalize_fio(name: str) -> str:
    if not name:
        return ""
    name = " ".join(str(name).split())
    return name.lower()


# ---------------------------------------------------------------------------
# Подбор комнаты (использует compute_available_rooms)
# ---------------------------------------------------------------------------
async def _find_room_id(db: AsyncSession, field_id: int, check_in: date, check_out: date) -> Optional[int]:
    groups = await compute_available_rooms(db, field_id, check_in, check_out)
    if not groups:
        logger.info("ROOM_PICK: field_id=%s %s–%s: свободных групп нет", field_id, check_in, check_out)
        return None
    best_group = max(groups, key=lambda g: (g["free_places"], -g["id"]))
    logger.info(
        "ROOM_PICK: field_id=%s %s–%s -> room_id=%s (room_number=%s), group_free=%s/%s",
        field_id, check_in, check_out, best_group["id"], best_group["room_number"],
        best_group["free_places"], best_group["capacity"],
    )
    return best_group["id"]


# ---------------------------------------------------------------------------
# Получение / создание сущностей
# ---------------------------------------------------------------------------
async def _get_or_create_field(db: AsyncSession, name: str, stats: ImportStats) -> Field:
    normalized = normalize_field_name(name)
    res = await db.execute(select(Field))
    for field_obj in res.scalars().all():
        if normalize_field_name(field_obj.name) == normalized:
            return field_obj
    raise HTTPException(404, "Не найдено месторождение")


async def _get_or_create_customer(db: AsyncSession, name: str, stats: ImportStats) -> Customer:
    name = (name or "—").strip() or "—"
    res = await db.execute(select(Customer).where(Customer.name.ilike(name)))
    customer = res.scalars().first()
    if customer is None:
        customer = Customer(name=name)
        db.add(customer)
        await db.flush()
        stats.customers_created.append(name)
        logger.info("CUSTOMER_CREATE: создан новый заказчик '%s' (id=%s)", name, customer.id)
    return customer


async def _get_or_create_resident(
    db: AsyncSession,
    full_name: str,
    position: Optional[str],
    stats: ImportStats,
    resident_cache: Dict[str, Resident],
) -> Resident:
    norm_name = normalize_fio(full_name)
    resident = resident_cache.get(norm_name)
    if resident is None:
        # Ищем в БД на случай, если в кэше нет
        stmt = select(Resident).where(func.lower(Resident.full_name) == norm_name)
        res = await db.execute(stmt)
        resident = res.scalars().first()
        if resident is None:
            resident = Resident(full_name=full_name, position=position, birthday=None)
            db.add(resident)
            await db.flush()
            stats.residents_created.append(full_name)
            logger.info("RESIDENT_CREATE: создан новый жилец '%s' (id=%s)", full_name, resident.id)
        resident_cache[norm_name] = resident
    return resident



async def _find_existing_requests(
    db: AsyncSession,
    row: ParsedRequestRow,
    field_id: int,
) -> List[Union[Request, Request_before]]:
    """
    Находит все активные (approved/pending) заявки для данного ФИО и месторождения
    в обеих таблицах.
    """
    norm_name = normalize_fio(row.full_name)
    results = []

    # 1. Формальные заявки (Request) – через Resident
    stmt_req = (
        select(Request)
        .join(Resident, Request.resident_id == Resident.id)
        .where(
            Request.field_id == field_id,
            func.lower(Resident.full_name) == norm_name,
            Request.status.in_(ACTIVE_REQUEST_STATUSES),
        )
    )
    req_res = await db.execute(stmt_req)
    results.extend(req_res.scalars().all())

    # 2. Гостевые заявки (Request_before) – напрямую по full_name
    stmt_before = (
        select(Request_before)
        .where(
            Request_before.field_id == field_id,
            func.lower(Request_before.full_name) == norm_name,
            Request_before.status.in_(ACTIVE_REQUEST_STATUSES),
        )
    )
    before_res = await db.execute(stmt_before)
    results.extend(before_res.scalars().all())

    logger.info("EXISTING_FOUND: %s field=%s count=%s", row.full_name, field_id, len(results))
    return results
# ---------------------------------------------------------------------------
# Импорт одной строки
# ---------------------------------------------------------------------------
async def _import_row(
    db: AsyncSession,
    row: ParsedRequestRow,
    user_id: int,
    stats: ImportStats,
    resident_cache: Dict[str, Resident],
    verbose: bool = True,
    allow_missing_contract: bool = False,
):
    # 1. Проверка обязательных полей
    if (not row.full_name or not str(row.full_name).strip() or
        not row.field_name or not str(row.field_name).strip() or
        not row.customer_name or not str(row.customer_name).strip() or
        not row.eol_fio or not str(row.eol_fio).strip() or
        not row.check_in or not row.check_out):
        stats.rows_skipped += 1
        stats.errors.append(
            f"Строка {row.full_name or 'неизвестно'}: отсутствуют обязательные поля "
            f"(ФИО, месторождение, заказчик, ЕОЛ, даты)"
        )
        logger.error("MISSING_REQUIRED_FIELDS: %s", row.full_name or "неизвестно")
        return

    # 2. Номер договора (если требуется)
    if not allow_missing_contract and (not row.contract_num or not str(row.contract_num).strip()):
        stats.rows_skipped += 1
        stats.errors.append(
            f"Строка {row.full_name or 'неизвестно'}: отсутствует номер договора, "
            f"а опция allow_missing_contract=False"
        )
        logger.error("MISSING_CONTRACT: %s", row.full_name or "неизвестно")
        return

    # 3. Инвертированные даты
    if row.check_in > row.check_out:
        stats.rows_skipped += 1
        stats.errors.append(
            f"{row.full_name}: дата заезда ({row.check_in}) позже даты выезда ({row.check_out})"
        )
        logger.error("INVALID_DATES: %s %s > %s", row.full_name, row.check_in, row.check_out)
        return

    # 4. Проверка на дату в прошлом (сегодня или будущее)
    today = date.today()
    if row.check_in < today:
        stats.expired_skipped += 1
        logger.info("EXPIRED_SKIP: %s check_in %s < today", row.full_name, row.check_in)
        if verbose:
            print(f"⏭️ пропущено (дата в прошлом): {row.full_name} ({row.check_in})")
        return

    # 5. Получение месторождения
    field_obj = await _get_or_create_field(db, row.field_name, stats)

    # 6. Поиск существующих активных заявок
    existing = await _find_existing_requests(db, row, field_obj.id)

    # 7. Проверка на точный дубликат
    exact_duplicate = any(
        r.check_in == row.check_in and r.check_out == row.check_out
        for r in existing
    )
    if exact_duplicate:
        stats.duplicates_skipped += 1
        logger.info("DUPLICATE_SKIP: точный дубликат для %s (%s-%s)", row.full_name, row.check_in, row.check_out)
        if verbose:
            print(f"⏭️ пропущен дубликат: {row.full_name} ({row.check_in}–{row.check_out})")
        return

    # 8. Пересекающиеся по датам – удаляем (замена)
    overlapping = [
        r for r in existing
        if r.check_in <= row.check_out and r.check_out >= row.check_in
    ]
    if overlapping:
        await _delete_requests(db, overlapping)
        logger.warning("REPLACED %s overlapping request(s) for %s", len(overlapping), row.full_name)
        if verbose:
            print(f"🔁 replaced {len(overlapping)} overlapping requests for {row.full_name}")

    # 9. Подбор комнаты через compute_available_rooms
    room_id = await _find_room_id(db, field_obj.id, row.check_in, row.check_out)
    if room_id is None:
        stats.rejected_no_room += 1
        logger.warning("NO_ROOM: %s field=%s %s-%s", row.full_name, field_obj.name, row.check_in, row.check_out)
        if verbose:
            print(f"❌ нет мест: {row.full_name} ({row.check_in}–{row.check_out})")
        return

    # 10. Номер договора (генерируем, если не передан)
    contract_num = row.contract_num.strip() if row.contract_num and str(row.contract_num).strip() else None
    if not contract_num:
        contract_num = await generate_contract_number(db, field_obj.name)
        logger.info("CONTRACT_GEN: сгенерирован новый номер %s для %s", contract_num, row.full_name)
    else:
        logger.info("CONTRACT_USE: использован номер из файла %s для %s", contract_num, row.full_name)

    # 11. Заказчик и жилец
    customer = await _get_or_create_customer(db, row.customer_name or "—", stats)
    resident = await _get_or_create_resident(db, row.full_name, row.position, stats, resident_cache)

    # 12. Создание формальной заявки (Request)
    new_req = Request(
        customer_id=customer.id,
        contract_num=contract_num,
        contract_date=row.contract_date,
        eol_fio=row.eol_fio,
        user_id=user_id,
        position=row.position,
        field_id=field_obj.id,
        check_in=row.check_in,
        check_out=row.check_out,
        days=(row.check_out - row.check_in).days + 1,
        room_id=room_id,
        status="approved",
        admin_comment=None,
        resident_id=resident.id,            
             
    )
    db.add(new_req)
    stats.approved_formal += 1
    if verbose:
        print(f"✅ FORMAL {row.full_name} -> комната {room_id} ({row.check_in}–{row.check_out})")

    await db.flush()

# ---------------------------------------------------------------------------
# Дедупликация внутри одного файла (убираем полностью одинаковые строки)
# ---------------------------------------------------------------------------
def make_row_key(row):
    return (
        normalize_fio(row.full_name),
        normalize_field_name(row.field_name),
        row.check_in,
        row.check_out,
        "formal" if row.is_full_form else "guest",
    )


def deduplicate_rows(rows):
    latest = {}
    for row in rows:
        latest[make_row_key(row)] = row
    return list(latest.values())


# ---------------------------------------------------------------------------
# Основная функция импорта
# ---------------------------------------------------------------------------
async def import_requests_from_excel(
    db: AsyncSession,
    wb_or_path,
    created_by_user_id: int,
    verbose: bool = True,
    allow_missing_contract: bool = False,
) -> ImportStats:
    stats = ImportStats()
    resident_cache: Dict[str, Resident] = {}

    logger.info("IMPORT_START: user_id=%s, allow_missing_contract=%s", created_by_user_id, allow_missing_contract)

    # Парсим Excel и дедуплицируем внутри файла
    rows = list(parse_workbook(wb_or_path))
    rows = deduplicate_rows(rows)

    for row in rows:
        try:
            # Вложенная транзакция для отката одной строки
            async with db.begin_nested():
                await _import_row(
                    db,
                    row,
                    created_by_user_id,
                    stats,
                    resident_cache,
                    verbose=verbose,
                    allow_missing_contract=allow_missing_contract,
                )
            # Фиксируем изменения после успешной обработки строки
            await db.commit()
        except Exception as exc:
            # Откат внутри begin_nested, но предыдущие строки уже сохранены
            stats.rows_skipped += 1
            error_text = f"{row.sheet_name} строка {row.row_number}: {exc}"
            stats.errors.append(error_text)
            logger.error("IMPORT_ROW_ERROR: %s", error_text, exc_info=True)
            if verbose:
                print(f"   ⚠️ Ошибка: {exc}")
            # Продолжаем со следующей строкой
            continue

    logger.info(
        "IMPORT_DONE: всего=%s, формальных=%s, гостевых=%s, отказов (нет мест)=%s, "
        "отказов (дата в прошлом)=%s, пропущено с ошибкой=%s, расхождений days=%s",
        len(rows), stats.approved_formal, stats.approved_guest,
        stats.rejected_no_room, stats.expired_skipped, stats.rows_skipped,
        len(stats.days_mismatch_warnings),
    )

    if verbose:
        print("\n" + "=" * 60)
        print(f"📊 ИТОГИ ИМПОРТА:")
        print(f"   ✅ Одобрено (формальных): {stats.approved_formal}")
        print(f"   ✅ Одобрено (гостевых):   {stats.approved_guest}")
        print(f"   ❌ Отклонено (нет мест):  {stats.rejected_no_room}")
        print(f"   ⏭️ Отклонено (дата в прошлом): {stats.expired_skipped}")
        print(f"   ⚠️ Пропущено с ошибкой:   {stats.rows_skipped}")
        if stats.fields_created:
            print(f"   🆕 Новые месторождения:   {stats.fields_created}")
        if stats.days_mismatch_warnings:
            print(f"   📌 Расхождений days:      {len(stats.days_mismatch_warnings)}")
        if stats.resident_overlap_warnings:
            print(f"   📌 Пересечений у жильцов: {len(stats.resident_overlap_warnings)}")
        if stats.errors:
            print(f"   📌 Первые ошибки: {stats.errors[:3]}")
        print("=" * 60)

    return stats