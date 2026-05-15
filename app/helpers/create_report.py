import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def create_report(dict_list: list, output_filename: str, sheet_name='расч.л'):
    if not os.path.exists('excel_files'):
        os.makedirs('excel_files')

    filepath = os.path.join('excel_files', output_filename)

    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    headers = ['Месторождение', 'Заказчик', 'ФИО проживающего',
               'Дата заезда', 'Дата выезда', 'Количество дней']
    ws.append(headers)

    for row in dict_list:
        ws.append([
            row['Месторождение'],
            row['Заказчик'],
            row['ФИО проживающего'],
            row['Дата заезда'].strftime("%d.%m.%Y"),
            row['Дата выезда'].strftime("%d.%m.%Y") if row['Дата выезда'] else "—",
            row['Количество дней']
        ])

    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    for cell in ws[1]:
        cell.font = Font(bold=True, name="Times New Roman", size=11)
        cell.fill = PatternFill("solid", fgColor="CCCCCC")
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border

    for row in ws.iter_rows(min_row=2):
        for i, cell in enumerate(row, start=1):
            cell.font = Font(name="Times New Roman", size=11)
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border
            if i in (4, 5, 6):
                cell.fill = PatternFill(start_color="86D472", end_color="86D472", fill_type="solid")

    widths = [25, 25, 30, 15, 15, 20]
    for i, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = width

    wb.save(filepath)
    return filepath