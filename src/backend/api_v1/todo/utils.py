import csv
import uuid
from asyncio import sleep
from datetime import datetime

import aiofiles
from openpyxl.styles import Side, Border
from openpyxl.workbook import Workbook

from backend.api_v1.todo.constants import TABLE_HEADER, STATUSES_MAP
from backend.api_v1.todo.models import Todo


def prepare_date(date: datetime) -> str | None:
    """
    Преобразование datetime в строку вида dd.mm.yyyy hh:mm:ss

    Parameters:
        date: объект datetime

    :return: строка вида dd.mm.yyyy hh:mm:ss или None
    """
    if not date:
        return

    return date.strftime('%d.%m.%Y %H:%M:%S')


def generate_tuple_from_todo(todo: Todo) -> tuple[str, str, str, str]:
    """
    Собирает кортеж из данных задачи

    Parameters:
        todo: экземпляр модели Todo
    :return: кортеж из данных задачи
    """
    return (
        todo.todo,
        todo.status,
        prepare_date(todo.created_date),
        prepare_date(todo.modified_date)
    )


async def get_report_to_csv(todos: list[Todo], user_id: uuid.UUID) -> dict[str, str]:
    """
    Формирует отчет по задачам пользователя в формате csv

    Parameters:
        todos: список задач
        user_id: идентификатор пользователя

    :return: данные о csv файле
    """
    path = f'/tmp/report_{user_id}.csv'
    async with aiofiles.open(file=path, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        await writer.writerow(TABLE_HEADER)
        for todo in todos:
            await writer.writerow(generate_tuple_from_todo(todo))
        file_info = {
            'path': path,
            'filename': f'report_{datetime.now().strftime("%d_%m_%Y")}.csv',
            'media_type': 'text/csv'
        }
        return file_info


async def get_report_to_xlsx(todos: list[Todo], user_id: uuid.UUID) -> dict[str, str]:
    """
        Формирует отчет по задачам пользователя в формате xlsx

        Parameters:
            todos: список задач
            user_id: идентификатор пользователя

        :return: данные о xlsx файле
        """
    path = f'/tmp/report_{user_id}.xlsx'

    work_book = Workbook()
    sheet = work_book.active
    sheet.title = 'Отчет'

    data = [generate_tuple_from_todo(todo) for todo in todos]
    dataset = sorted(data, key=lambda item: STATUSES_MAP[item[1]])  # Сортируем по статусу
    dataset.insert(0, TABLE_HEADER)

    for row in dataset:
        sheet.append(row)

    sheet.append([])  # Добавляем пустую строку

    sheet.append(['Всего задач: ', len(todos)])

    thin = Side(border_style="thin", color="000000")  # Стиль рамки

    # Задаем ширину ячеек по содержимому и чертим рамки
    for column in sheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
            cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)

        adjusted_width = (max_length + 2) * 1.2
        sheet.column_dimensions[column_letter].width = adjusted_width

    # Отдаем управление event_loop'у (имитация корутины)
    await sleep(0)

    work_book.save(path)

    file_info = {
        'path': path,
        'filename': f'report_{datetime.now().strftime("%d_%m_%Y")}.xlsx',
        'media_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
    return file_info
