"""
Загрузка распарсенной Excel-заявки с подробным логированием.

Логика подсчёта свободных мест НЕ дублируется здесь — используется единая
функция compute_available_rooms() из app/routers/requests.py, которая же
отдаёт доступность через эндпоинт /api/requests/available. Это гарантирует,
что ручное создание заявки и Excel-импорт всегда видят одну и ту же
картину занятости комнат.
"""

from __future__ import annotations

import logging
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Customer, Field, Request, Request_before, Resident, Room
from app.excel_parser import ParsedRequestRow, parse_workbook
from app.utils import generate_contract_number
from app.routers.requests import compute_available_rooms

logger = logging.getLogger("excel_import")

DEFAULT_GPNV_CUSTOMER_NAME = "ООО «Газпромнефть-Восток»"
NO_ROOM_COMMENT = "Нет свободных мест на запрошенный период"
DUPLICATE_COMMENT = "Пропущено: дубликат уже существующей заявки"


@dataclass
class ImportStats:
    approved_formal: int = 0
    approved_guest: int = 0
    rejected_no_room: int = 0
    duplicates_skipped: int = 0
    rows_skipped: int = 0
    customers_created: list[str] = field(default_factory=list)
    fields_created: list[str] = field(default_factory=list)
    residents_created: list[str] = field(default_factory=list)
    resident_overlap_warnings: list[str] = field(default_factory=list)
    days_mismatch_warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Нормализация названий месторождений
# ---------------------------------------------------------------------------
def normalize_field_name(name: str) -> str:
    """
    Приводим разные варианты названий месторождений к одному виду, чтобы
    "Шингинское", "шингинское", "Шингинское месторождение", "Шингинское "
    (с обычным или неразрывным пробелом), "Шингинское." и т.п. матчились
    в одно и то же Field, а не плодили дубликаты.
    """

    if not name:
        return ""

    name = str(name)

    # NBSP (\xa0) и другие невидимые юникод-пробелы -> обычный пробел
    name = name.replace("\xa0", " ")
    name = "".join(
        " " if unicodedata.category(ch) == "Zs" else ch
        for ch in name
    )

    name = name.lower()

    # Частые "хвосты", не несущие различительного смысла
    name = name.replace("месторождение", "")
    name = name.replace("месторожд.", "")
    name = name.replace("месторожд", "")
    name = name.replace("гпн", "")
    name = name.replace('"', "")
    name = name.replace("«", "")
    name = name.replace("»", "")

    # Точки/запятые на конце слова, как мусор после сокращений
    name = re.sub(r"[.,]+", "", name)

    # Любые управляющие/проблемные символы (\n, \t, \r) -> пробел
    name = re.sub(r"[\r\n\t]+", " ", name)

    name = re.sub(r"\s+", " ", name)

    return name.strip()

def normalize_fio(name: str) -> str:
    """Приводит ФИО к каноническому виду для дедупликации."""
    if not name:
        return ""
    name = " ".join(str(name).split())  # убираем лишние пробелы
    return name.lower()

# ---------------------------------------------------------------------------
# Подбор комнаты — переиспользуем единую логику из app/requests.py
# ---------------------------------------------------------------------------
async def _find_room_id(db: AsyncSession, field_id: int, check_in: date, check_out: date) -> Optional[int]:
    """
    Возвращает room_id комнаты с максимальной балансировкой свободных мест,
    либо None, если свободных мест нет. Использует ту же функцию, что и
    ручной API /api/requests/available — никакой отдельной логики подсчёта
    мест здесь больше нет (раньше была отдельная копия с багами).
    """
    groups = await compute_available_rooms(db, field_id, check_in, check_out)
    if not groups:
        logger.info(
            "ROOM_PICK: field_id=%s %s–%s: свободных групп нет",
            field_id, check_in, check_out,
        )
        return None

    # compute_available_rooms уже выбрал внутри каждой группы лучший вариант
    # (максимум свободных мест). Среди групп тоже берём ту, где сейчас больше
    # всего свободных мест — это дополнительно сглаживает заполнение при
    # массовом импорте многих строк подряд.
    best_group = max(groups, key=lambda g: (g["free_places"], -g["id"]))
    logger.info(
        "ROOM_PICK: field_id=%s %s–%s -> room_id=%s (room_number=%s), "
        "group_free=%s/%s",
        field_id, check_in, check_out, best_group["id"], best_group["room_number"],
        best_group["free_places"], best_group["capacity"],
    )
    return best_group["id"]


# ---------------------------------------------------------------------------
# find-or-create справочников
# ---------------------------------------------------------------------------

async def _get_or_create_field(
    db: AsyncSession,
    name: str,
    stats: ImportStats,
) -> Field:

    normalized = normalize_field_name(name)

    res = await db.execute(select(Field))
    fields = res.scalars().all()

    for field_obj in fields:
        if normalize_field_name(field_obj.name) == normalized:
            logger.debug(
                "FIELD_MATCH: '%s' -> существующее месторождение id=%s ('%s')",
                name, field_obj.id, field_obj.name,
            )
            return field_obj

    field_obj = Field(name=name.strip())
    db.add(field_obj)
    await db.flush()

    stats.fields_created.append(name)
    logger.warning(
        "FIELD_CREATE: создано НОВОЕ месторождение '%s' (id=%s, normalized='%s') — "
        "проверьте, не опечатка ли это в Excel",
        name, field_obj.id, normalized,
    )

    return field_obj


async def _get_or_create_customer(
    db: AsyncSession,
    name: str,
    stats: ImportStats,
) -> Customer:
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
    db: AsyncSession, full_name: str, position: Optional[str], stats: ImportStats
) -> Resident:
    res = await db.execute(select(Resident).where(Resident.full_name.ilike(full_name)))
    resident = res.scalars().first()
    if resident is None:
        resident = Resident(full_name=full_name, position=position, birthday=None)
        db.add(resident)
        await db.flush()
        stats.residents_created.append(full_name)
        logger.info("RESIDENT_CREATE: создан новый жилец '%s' (id=%s)", full_name, resident.id)
    return resident


def _contract_comment(row: ParsedRequestRow) -> Optional[str]:
    if not row.contract_num:
        return None
    if row.contract_date:
        return f"Договор по заявке: {row.contract_num} от {row.contract_date.strftime('%d.%m.%Y')}"
    return f"Договор по заявке: {row.contract_num}"




# ---------------------------------------------------------------------------
# Проверка пересечения по Resident (информационная, не блокирующая)
# ---------------------------------------------------------------------------
async def _warn_if_resident_overlaps(
    db: AsyncSession,
    resident_id: int,
    full_name: str,
    check_in: date,
    check_out: date,
    stats: ImportStats,
) -> None:
    """
    Согласовано: один Resident МОЖЕТ иметь пересекающиеся по датам заявки —
    это не блокируется. Но мы логируем такие случаи как warning, чтобы их
    можно было вручную проверить после импорта (см.
    stats.resident_overlap_warnings и логи RESIDENT_OVERLAP).
    """
    res = await db.execute(
        select(Request.id, Request.check_in, Request.check_out, Request.room_id)
        .where(
            Request.resident_id == resident_id,
            Request.status.in_(("approved", "pending")),
            Request.check_in < check_out,
            Request.check_out > check_in,
        )
    )
    overlaps = res.all()
    if overlaps:
        details = [(r.id, str(r.check_in), str(r.check_out), r.room_id) for r in overlaps]
        msg = (
            f"resident_id={resident_id} ('{full_name}'): новая заявка "
            f"{check_in}–{check_out} пересекается с {len(overlaps)} существующей(ими) "
            f"заявкой(ами): {details}"
        )
        stats.resident_overlap_warnings.append(msg)
        logger.warning("RESIDENT_OVERLAP: %s", msg)


# ---------------------------------------------------------------------------
# Обработка одной строки с логированием
# ---------------------------------------------------------------------------
ACTIVE_REQUEST_STATUSES = ("approved", "pending")


async def _find_resident(
    db: AsyncSession,
    full_name: str,
) -> Resident | None:

    res = await db.execute(
        select(Resident).where(
            Resident.full_name.ilike(full_name.strip())
        )
    )
    return res.scalars().first()

async def _find_existing_requests(
    db: AsyncSession,
    row,
    field_id: int,
):
    """
    Ищем пересекающиеся заявки.
    """
    if row.is_full_form:
        resident = await _find_resident(db, row.full_name)
        if not resident:
            return []
        q = (
            select(Request)
            .where(
                Request.resident_id == resident.id,
                Request.field_id == field_id,
                Request.status.in_(ACTIVE_REQUEST_STATUSES)
            )
        )
    else:
        q = (
            select(Request_before)
            .where(
                Request_before.full_name == row.full_name,
                Request_before.field_id == field_id,
                Request_before.status.in_(ACTIVE_REQUEST_STATUSES),
            )
        )
    
    res = await db.execute(q)
    existing = res.scalars().all()

    # 👇 НОВЫЙ ЛОГ – показывает, сколько пересекающихся заявок найдено
    logger.info(
        "EXISTING_FOUND: %s field=%s count=%s",
        row.full_name,
        field_id,
        len(existing),
    )

    return existing


async def _delete_requests(db, requests):
    for r in requests:
        await db.delete(r)
    await db.flush()


async def _import_row(db, row, user_id, stats, verbose=True):
    logger.warning("DEBUG: contract_num=%r, eol_fio=%r", row.contract_num, row.eol_fio)
    if (not row.full_name or not str(row.full_name).strip() or
        not row.field_name or not str(row.field_name).strip() or
        not row.customer_name or not str(row.customer_name).strip() or
        not row.contract_num or not str(row.contract_num).strip() or
        not row.eol_fio or not str(row.eol_fio).strip() or
        not row.check_in or not row.check_out):
        
        stats.rows_skipped += 1
        stats.errors.append(
            f"Строка {row.full_name or 'неизвестно'}: отсутствуют обязательные поля "
            f"(ФИО, месторождение, заказчик, договор, ЕОЛ, даты)"
        )
        logger.error("MISSING_REQUIRED_FIELDS: %s", row.full_name or "неизвестно")
        return
    field_obj = await _get_or_create_field(db, row.field_name, stats)
    if row.check_in > row.check_out:
        stats.rows_skipped += 1

        logger.error(
            "INVALID_RANGE: %s (%s > %s)",
            row.full_name,
            row.check_in,
            row.check_out,
        )

        stats.errors.append(
            f"{row.full_name}: дата заезда позже даты выезда"
        )

        return
    existing = await _find_existing_requests(
        db,
        row,
        field_obj.id,
    )
    print(
        f"CHECK: {row.full_name} "
        f"{row.check_in} - {row.check_out}"
    )

    for r in existing:
        print(
            f"FOUND: id={r.id} "
            f"{r.check_in} - {r.check_out}"
        )

        print(
            "EQUAL:",
            r.check_in == row.check_in,
            r.check_out == row.check_out,
        )
    logger.info(
        "CHECK_DUPLICATE: %s %s-%s",
        row.full_name,
        row.check_in,
        row.check_out,
    )
    logger.warning(
        "DUP_CHECK row=%s %s-%s",
        row.full_name,
        row.check_in,
        row.check_out,
    )

    for r in existing:
        logger.warning(
            "EXISTING row=%s %s-%s id=%s",
            row.full_name,
            r.check_in,
            r.check_out,
            r.id,
        )

        logger.warning(
            "COMPARE in=%s out=%s",
            r.check_in == row.check_in,
            r.check_out == row.check_out,
        )
    # EXACT DUPLICATE
    for r in existing:
        if (
            r.check_in == row.check_in
            and r.check_out == row.check_out
        ):
            stats.duplicates_skipped += 1

            logger.info(
                "EXACT_DUPLICATE_SKIP: %s %s–%s",
                row.full_name,
                row.check_in,
                row.check_out,
            )

            if verbose:
                print(f"⏭️ exact duplicate skipped: {row.full_name}")

            return

    # REPLACE
    if existing:
        await _delete_requests(db, existing)

        logger.warning(
            "REPLACED %s old request(s) for %s",
            len(existing),
            row.full_name,
        )

        if verbose:
            print(
                f"🔁 replaced {len(existing)} old requests for {row.full_name}"
            )


    room_id = await _find_room_id(db, field_obj.id, row.check_in, row.check_out)

    if room_id is None:
        logger.warning(
            "NO_ROOM: %s field=%s %s-%s",
            row.full_name,
            field_obj.name,
            row.check_in,
            row.check_out,
        )
        stats.rejected_no_room += 1
        return
    
    
    contract_num = await generate_contract_number(db, field_obj.name)

    
    customer = await _get_or_create_customer(db, row.customer_name or "—", stats)
    resident = await _get_or_create_resident(db, row.full_name, row.position, stats)

    db.add(Request(
        customer_id=customer.id,
        contract_num=contract_num,
        contract_date=row.contract_date,
        eol_fio=row.eol_fio,
        user_id=user_id,
        position=row.position,
        field_id=field_obj.id,
        check_in=row.check_in,
        check_out=row.check_out,
        days=row.days,
        room_id=room_id,
        status="approved",
        resident_id=resident.id,
    ))

    stats.approved_formal += 1

    if verbose:
        print(f"✅ FORMAL {row.full_name} -> room {room_id}")
    await db.flush()

def make_row_key(row):
    if row.is_full_form:
        return (
            normalize_fio(row.full_name),
            normalize_field_name(row.field_name),
            "formal",
        )

    return (
        normalize_fio(row.full_name),
        normalize_field_name(row.field_name),
        "guest",
    )    
def deduplicate_rows(rows):
    latest = {}

    for row in rows:
        latest[make_row_key(row)] = row

    return list(latest.values())
async def import_requests_from_excel(
    db: AsyncSession,
    wb_or_path,
    created_by_user_id: int,
    verbose: bool = True,
) -> ImportStats:
    """
    Импорт заявок из Excel с подробным логированием (через logging и,
    опционально, print при verbose=True).

    ВАЖНО про последовательность: строки обрабатываются строго по очереди
    (не параллельно), каждая в своей db.begin_nested(). Подбор комнаты
    (_find_room_id -> compute_available_rooms) видит уже зафлешенные
    (db.flush()) предыдущие строки этого же импорта через обычные SELECT
    с group_by — поэтому 5 человек подряд в комнату на 4 места корректно
    дадут 4 approved + 1 rejected, а не 5 approved.
    """
    stats = ImportStats()
    row_count = 0

    logger.info("IMPORT_START: начало импорта, user_id=%s", created_by_user_id)
    rows = list(parse_workbook(wb_or_path))

    rows = deduplicate_rows(rows)
        
    for row in rows:
        row_count += 1
        try:
            async with db.begin_nested():
                await _import_row(db, row, created_by_user_id, stats, verbose=verbose)
        except Exception as exc:
            stats.rows_skipped += 1
            error_text = f"{row.sheet_name} строка {row.row_number}: {exc}"
            stats.errors.append(error_text)
            logger.error("IMPORT_ROW_ERROR: %s", error_text, exc_info=True)
            if verbose:
                print(f"   ⚠️ Ошибка: {exc}")
            continue

    await db.commit()

    logger.info(
        "IMPORT_DONE: всего строк=%s, формальных=%s, гостевых=%s, отказов=%s, "
        "дубликатов=%s, ошибок=%s, расхождений days=%s, пересечений resident=%s",
        row_count, stats.approved_formal, stats.approved_guest, stats.rejected_no_room,
        stats.duplicates_skipped, stats.rows_skipped,
        len(stats.days_mismatch_warnings), len(stats.resident_overlap_warnings),
    )

    if verbose:
        print("\n" + "=" * 60)
        print(f"📊 ИТОГИ ИМПОРТА:")
        print(f"   ✅ Одобрено (формальных): {stats.approved_formal}")
        print(f"   ✅ Одобрено (гостевых):   {stats.approved_guest}")
        print(f"   ❌ Отклонено (нет мест):  {stats.rejected_no_room}")
        print(f"   ⏭️ Пропущено (дубликат):  {stats.duplicates_skipped}")
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