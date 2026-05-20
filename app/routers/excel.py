from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import io
from openpyxl import load_workbook
from app.database import get_db
from app.models import Field, Customer, Location, Path, Workplace, Room, Resident, ResidentDay
from app.excel_parser import parse_all_months
from app.core.dependencies import get_current_user
from datetime import date
router = APIRouter()

@router.post("/api/upload_excel")
async def upload_excel(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    # user=Depends(get_current_user)
):
    if not file.filename.endswith((".xlsx", ".xls")):
        return JSONResponse({"error": "Неверный формат файла"}, status_code=400)

    try:
        base_name = file.filename.rsplit(".", 1)[0].strip()
        parts = base_name.split("_")
        field_name = parts[0]
        year = int(parts[1]) 
        if year < 2000:
            return JSONResponse({"error": "Имя файла должно быть вида Урманское_2025.xlsx"}, status_code=400)
    except (IndexError, ValueError):
        return JSONResponse({"error": "Имя файла должно быть вида Урманское_2025.xlsx"}, status_code=400)

    try:
        contents = await file.read()
        wb = load_workbook(io.BytesIO(contents), data_only=False)
        all_records = list(parse_all_months(wb, year=year))

        errors = []
        total = 0

        # Кэши
        customer_cache = {c.name: c.id for c in (await db.execute(select(Customer))).scalars()}
        location_cache = {l.name: l.id for l in (await db.execute(select(Location))).scalars()}
        path_cache = {p.description: p.id for p in (await db.execute(select(Path))).scalars()}
        workplace_cache = {w.name: w.id for w in (await db.execute(select(Workplace))).scalars()}
        room_cache = {r.room_number + r.room_unique_id: r.id for r in (await db.execute(select(Room))).scalars()}

        res = await db.execute(select(Field).where(Field.name == field_name))
        field = res.scalars().first()
        if not field:
            field = Field(name=field_name)
            db.add(field)
            await db.flush()
        field_id = field.id

        for rec in all_records:
            customer_name = rec.get("customer") or "Неизвестно"
            location_name = rec.get("расположение") or "-"
            path_desc = rec.get("путь") or "-"
            workplace_name = rec.get("workplace") or "—"

            if workplace_name != "—" and workplace_name not in workplace_cache:
                workplace_obj = Workplace(name=workplace_name)
                db.add(workplace_obj)
                workplace_cache[workplace_name] = workplace_obj
            if customer_name not in customer_cache:
                customer_obj = Customer(name=customer_name)
                db.add(customer_obj)
                customer_cache[customer_name] = customer_obj
            if location_name not in location_cache:
                location_obj = Location(name=location_name)
                db.add(location_obj)
                location_cache[location_name] = location_obj
            if path_desc not in path_cache:
                path_obj = Path(description=path_desc)
                db.add(path_obj)
                path_cache[path_desc] = path_obj

        await db.flush()

        workplace_cache = {k: (v.id if hasattr(v, 'id') else v) for k, v in workplace_cache.items()}
        customer_cache = {k: (v.id if hasattr(v, 'id') else v) for k, v in customer_cache.items()}
        location_cache = {k: (v.id if hasattr(v, 'id') else v) for k, v in location_cache.items()}
        path_cache = {k: (v.id if hasattr(v, 'id') else v) for k, v in path_cache.items()}

        for rec in all_records:
            room_name = rec.get("комната") or "—"
            room_uid = rec.get("room_unique_id") or ""
            room_cache_key = room_name + room_uid
            if room_cache_key in room_cache:
                continue
            room_obj = Room(
                room_number=room_name,
                capacity=int(rec.get("мест")) if rec.get("мест") else 0,
                field_id=field_id,
                location_id=location_cache.get(rec.get("расположение") or "-"),
                path_id=path_cache.get(rec.get("путь") or "-"),
                room_unique_id=room_uid or None
            )
            db.add(room_obj)
            room_cache[room_cache_key] = room_obj

        await db.flush()
        room_cache = {k: (v.id if hasattr(v, 'id') else v) for k, v in room_cache.items()}
        await db.commit()

        pending = 0
        for rec in all_records:
            try:
                async with db.begin_nested():
                    workplace_id = workplace_cache.get(rec.get("workplace") or "—")
                    customer_id = customer_cache.get(rec.get("customer") or "Неизвестно")
                    room_cache_key = (rec.get("комната") or "—") + (rec.get("room_unique_id") or "")
                    room_id = room_cache.get(room_cache_key)
                    gender_raw = rec.get("пол", "")
                    gender = "М" if isinstance(gender_raw, str) and gender_raw.lower().startswith("муж") else "Ж"
                    check_in : date = rec['days'][0][0] 
                    check_out : date = rec['days'][-1][1]
                    
                    resident = Resident(
                        field_id=field_id,
                        customer_id=customer_id,
                        full_name=rec["full_name"],
                        position=rec.get("position", ""),
                        check_in=check_in or None,
                        check_out=check_out or None,
                        gender=gender,
                        room_id=room_id,
                        shift=rec.get("смена", ""),
                    )
                    db.add(resident)
                    await db.flush()
                    
                    for x in rec['days']:
                        check_in : date = x[0]
                        check_out : date = x[1]
                        db.add(ResidentDay(
                            resident_id=resident.id,
                            date=check_in,
                            extra=check_out,
                            customer_id=customer_id,
                            room_id=room_id,
                            workplace_id=workplace_id,
                            days=int((check_out-check_in).days + 1)
                        ))
                    
                    total += 1
                    
            except Exception as e:
                errors.append({"record": rec.get("full_name", "?"), "error": str(e)})

        await db.commit()
        
        return {
            "message": f"Загружено {total} записей," + (f", пропущено: {len(errors)}" if errors else ""),
            "errors": errors[:20],
        }
    except Exception as e:
        await db.rollback()
        return JSONResponse({"error": str(e)}, status_code=500)