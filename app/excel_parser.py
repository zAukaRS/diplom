"""
Парсер Excel-файла с расселением по общежитию.

Структура листа (например, 'июнь'):
  Колонки:
    A  - Расположение     (ffill)
    B  - Путь             (ffill)
    C  - № комнаты        (ffill)
    D  - К-во мест        (ffill)
    E  - Пол
    F  - ФИО              (может содержать 1-N имён через '/')
    G  - Должность        (может содержать 1-N должностей через '/')
    H  - Смена
    I–AM (cols 9–39) - дни 1–31: значение = название заказчика, None = жильец отсутствует
    AO - Место работы     (дополнительный столбец)

Логика разделения жильцов:
  • 1 имя  → 1 запись.
  • N имён, блоков >= N по (значение+цвет) → i-е имя ↔ i-й блок (посменная работа).
  • N имён, 1 блок, 1 цвет → все жили одновременно, каждый получает весь диапазон.

Цвет ячейки:
  Когда заказчик одинаковый, но жильцы разные — Excel-файл размечает ячейки
  разными цветами заливки. Функция _contiguous_blocks учитывает смену цвета
  как границу между жильцами, даже если значение не менялось.
"""

from __future__ import annotations

import io
from datetime import date, timedelta
from typing import Generator

from openpyxl import load_workbook
from openpyxl.cell import Cell

# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------

DAY_COL_START = 9   # 1-based, колонка I = день 1
DAY_COL_END   = 39  # колонка AM = день 31 (включительно)


def _cell_color(cell: Cell) -> str | None:
    """
    Возвращает RGB-строку цвета заливки ячейки ('FFFF00', 'FF0000', ...)
    или None если заливки нет / прозрачная.
    """
    try:
        fill = cell.fill
        if fill.fill_type == "solid":
            color = fill.fgColor
            if color.type == "rgb":
                rgb = color.rgb  # вида 'FFRRGGBB' или 'RRGGBB'
                # Убираем alpha-канал если есть, и отсеиваем "нет цвета"
                rgb_clean = rgb[-6:] if len(rgb) == 8 else rgb
                if rgb_clean not in ("000000", "FFFFFF", "ffffff"):
                    return rgb_clean
            elif color.type == "theme":
                # theme-цвет тоже считаем маркером — кодируем как строку
                return f"theme:{color.theme}:{color.tint:.3f}"
    except Exception:
        pass
    return None


def _contiguous_blocks(
    day_cells: list[Cell],
) -> list[tuple[int, int, str]]:
    """
    Возвращает список (day_start, day_end, customer) непрерывных блоков.
    day_start и day_end – номера дней (1-based), оба включительно.

    Блок разрывается когда:
      1. Значение ячейки становится None (жилец уехал)
      2. Значение меняется (другой заказчик)
      3. Цвет заливки меняется (тот же заказчик, но другой жилец)
    """
    blocks: list[tuple[int, int, str,str,int]] = []
    in_block = False
    start = 0
    cur_val = None
    cur_color = None

    for i, cell in enumerate(day_cells):
        v = cell.value
        color = _cell_color(cell)

        if v is not None and not in_block:
            # Начало нового блока
            in_block = True
            start = i
            cur_val = v
            cur_color = color

        elif in_block:
            val_changed   = (v is None or v != cur_val)
            color_changed = (color != cur_color) and (color is not None or cur_color is not None)

            if val_changed or color_changed:
                blocks.append((start + 1, i, cur_val,cur_color,i-start))
                if v is not None:
                    start = i
                    cur_val = v
                    cur_color = color
                else:
                    in_block = False

    if in_block:
        blocks.append((start + 1, len(day_cells), cur_val,cur_color,len(day_cells)-start))

    return blocks


def _split_slash(value: str | None, n: int) -> list[str]:
    """Разбивает строку через '/', возвращает ровно n элементов."""
    if not value:
        return [""] * n
    parts = [p.strip() for p in str(value).split("/")]
    if len(parts) >= n:
        return parts[:n]
    # Если частей меньше — дублируем последнюю
    while len(parts) < n:
        parts.append(parts[-1])
    return parts



def parse_sheet(
    wb_or_path,
    sheet_name: str,
    year: int,
    month: int,
) -> Generator[dict, None, None]:
    """
    Генератор: для каждого жильца на листе возвращает словарь:

        {
            "расположение": str,
            "путь": str,
            "комната": str,
            "пол": str,
            "смена": str,
            "full_name": str,
            "position": str,
            "customer": str,      
            "check_in": date,
            "check_out": date,
            "days": int,
        }
    """
    if isinstance(wb_or_path, (str, bytes)):
        wb = load_workbook(wb_or_path, data_only=False)
    elif hasattr(wb_or_path, "read"):
        content = wb_or_path.read()
        wb = load_workbook(io.BytesIO(content), data_only=False)
    else:
        wb = wb_or_path

    sheet = wb[sheet_name]

    # Контекстные переменные (ffill)
    ctx_location = ""
    ctx_path = ""
    ctx_room = ""
    ctx_seats = ""
    ctx_room_unique = "" 
    list_of_rooms = []
    
    for _, row in enumerate(
        sheet.iter_rows(min_row=2, max_row=sheet.max_row), start=2
    ):
        # --- ffill контекстных колонок ---
        def cv(col_0idx):
            v = row[col_0idx].value
            return str(v).strip() if v not in (None, "") else None
        
        if cv(0):
            ctx_location = cv(0)
        if cv(1):
            ctx_path = cv(1)
        if cv(2):
            list_of_rooms = []
            ctx_room = cv(2)
        if cv(3) and cv(2):
            ctx_seats = cv(3)
            ctx_room_unique = cv(3) +'a'
            list_of_rooms.append(ctx_room_unique)
        elif cv(3):
            ctx_seats = cv(3)
            ctx_room_unique = cv(3)
            if ctx_room_unique+'a' in list_of_rooms:
                for x in 'bcdefg':
                    if ctx_room_unique+x not in list_of_rooms:
                        ctx_room_unique = ctx_room_unique + x
                        list_of_rooms.append(ctx_room_unique)
                        break
            else:
                ctx_room_unique = cv(3)+'a' 
                list_of_rooms.append(ctx_room_unique)
        
        fio_raw = cv(5)
        if not fio_raw:
            continue  # пустая строка

        position_raw = cv(6)
        shift = cv(7) or ""

        # Дни: индексы 8..38 (0-based) = колонки I..AM = дни 1..31
        # Передаём сами ячейки — нужны и значения и цвет заливки
        day_cells = [row[c] for c in range(8, 39)]

        blocks = _contiguous_blocks(day_cells)

        if not blocks:
            continue  # жилец отсутствовал весь месяц — пропускаем

        # Список имён
        names = [n.strip() for n in fio_raw.split("/") if n.strip()]
        n = len(names)
        positions = _split_slash(position_raw, n)

        if n == 1:
            dayss  : int = 0
            for x in blocks:
                dayss += x[-1]
            # Один жилец ИЛИ блоков меньше чем имён — весь диапазон общий
            all_start = blocks[0][0]
            all_end = blocks[-1][1]
            combined_customer = blocks[0][2]  # первый заказчик (упрощение)
            for i, name in enumerate(names):
                check_in = date(year, month, all_start)
                check_out = date(year, month, min(all_end, _days_in_month(year, month)))
                yield {
                    "расположение": ctx_location,
                    "путь": ctx_path,
                    "комната": ctx_room,
                    "мест": ctx_seats[:-1],
                    "пол": cv(4) or "",
                    "смена": shift,
                    "full_name": name,
                    "position": positions[i],
                    "customer": combined_customer,
                    "check_in": check_in,
                    "check_out": check_out,
                    "days": dayss,
                    "room_unique_id" : ctx_room_unique,
                    "workplace" : cv(40)
                }
        else:
            # N имён ↔ N блоков
            bocks = [(blocks[0])]
            if len(blocks) > n:
                color_st = blocks[0][-2]
                for x in range(1,len(blocks)):
                    if blocks[x][-2] == color_st and color_st is not None:
                        bocks[-1] = (bocks[-1][0],blocks[x][1],bocks[-1][2],color_st,bocks[-1][-1]+blocks[x][-1])
                    else:
                        bocks.append(blocks[x])
                    color_st = blocks[x][-2]

                blocks = bocks if len(bocks) == n else []

            for i, name in enumerate(names):
                if len(blocks) != n:
                    break
                b_start, b_end, customer = blocks[i][0],blocks[i][1],blocks[i][2]
                check_in = date(year, month, b_start)
                check_out = date(year, month, min(b_end, _days_in_month(year, month)))
                yield {
                    "расположение": ctx_location,
                    "путь": ctx_path,
                    "комната": ctx_room,
                    "мест": ctx_seats[:-1],
                    "пол": cv(4),
                    "смена": shift,
                    "full_name": name,
                    "position": positions[i],
                    "customer": customer,
                    "check_in": check_in,
                    "check_out": check_out,
                    "days": (check_out - check_in).days + 1,
                    "room_unique_id" : ctx_room_unique,
                    "workplace" : cv(40)
                }


def _days_in_month(year: int, month: int) -> int:
    if month == 12:
        return 31
    return (date(year, month + 1, 1) - timedelta(days=1)).day


# ---------------------------------------------------------------------------
# Хелпер: все листы месяцев
# ---------------------------------------------------------------------------

MONTHS_RU = {
    "январь": 1, "февраль": 2, "март": 3, "апрель": 4,
    "май": 5, "июнь": 6, "июль": 7, "август": 8,
    "сентябрь": 9, "октябрь": 10, "ноябрь": 11, "декабрь": 12,
}


def parse_all_months(wb_or_path, year: int) -> Generator[dict, None, None]:
    """Перебирает все листы-месяцы в книге."""
    if isinstance(wb_or_path, (str, bytes)):
        wb = load_workbook(wb_or_path, data_only=False)
    elif hasattr(wb_or_path, "read"):
        content = wb_or_path.read()
        wb = load_workbook(io.BytesIO(content), data_only=False)
    else:
        wb = wb_or_path

    for sheet_name in wb.sheetnames:
        normalized = sheet_name.strip().lower().replace(" ", "")
        for ru_month, month_num in MONTHS_RU.items():
            if ru_month in normalized:
                yield from parse_sheet(wb, sheet_name, year, month_num)
                break


