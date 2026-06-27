# app/room_importer.py
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Location, Path, Room
from .simple_room_importer import import_rooms_from_excel, ImportResult 

async def apply_to_db_async(
    result: ImportResult,
    db: AsyncSession,
    field_id: int,
    skip_existing: bool = True,
) -> dict:
    """
    Асинхронное сохранение результатов парсинга в БД.
    Возвращает статистику: {'locations': N, 'paths': N, 'rooms': N, 'skipped': N}
    """
    stats = {"locations": 0, "paths": 0, "rooms": 0, "skipped": 0}

    # --- Locations ---
    location_map: dict[str, int] = {}
    for loc_row in result.locations:
        existing = await db.execute(select(Location).where(Location.name == loc_row.name))
        existing_loc = existing.scalar_one_or_none()
        if existing_loc:
            location_map[loc_row.name] = existing_loc.id
            if skip_existing:
                stats["skipped"] += 1
                continue
        loc = Location(name=loc_row.name)
        db.add(loc)
        await db.flush()
        location_map[loc_row.name] = loc.id
        stats["locations"] += 1

    # --- Paths ---
    path_map: dict[str, int] = {}
    for path_row in result.paths:
        existing = await db.execute(select(Path).where(Path.description == path_row.description))
        existing_path = existing.scalar_one_or_none()
        if existing_path:
            path_map[path_row.description] = existing_path.id
            if skip_existing:
                stats["skipped"] += 1
                continue
        p = Path(description=path_row.description)
        db.add(p)
        await db.flush()
        path_map[path_row.description] = p.id
        stats["paths"] += 1

    # --- Rooms ---
    for room_row in result.rooms:
        existing = await db.execute(
            select(Room).where(
                Room.room_unique_id == room_row.room_unique_id,
                Room.field_id == field_id,
            )
        )
        existing_room = existing.scalar_one_or_none()
        if existing_room and skip_existing:
            stats["skipped"] += 1
            continue

        loc_id = location_map.get(room_row.location_name)
        path_id = path_map.get(room_row.path_description)

        r = Room(
            room_number=room_row.room_number,
            capacity=room_row.capacity,
            room_unique_id=room_row.room_unique_id,
            field_id=field_id,
            location_id=loc_id,
            path_id=path_id,
            status=room_row.status,
        )
        db.add(r)
        stats["rooms"] += 1

    await db.commit()
    return stats