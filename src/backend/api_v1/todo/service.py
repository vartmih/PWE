import uuid
from datetime import datetime
from typing import Union

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api_v1.todo.models import Todo, Status
from backend.api_v1.todo.query_params import ReportQueryParams
from backend.api_v1.todo.schemas import TodoCreateSchema, TodoUpdateSchema
from backend.api_v1.todo.utils import get_report_to_csv, get_report_to_xlsx
from backend.api_v1.user.models import User


async def get_statuses(session: AsyncSession) -> list[Status]:
    """
    Возвращает список всех статусов

    Parameters:
        session: асинхронная сессия для работы с базой данных

    :return: список всех статусов
    """
    status_query = select(Status)
    statuses = await session.scalars(status_query)
    return list(statuses)


async def get_todos(user: User) -> list[Todo | None]:
    """
    Возвращает список всех задач

    Parameters:
        user: авторизованный пользователь

    :return: список всех задач
    """
    return user.todos


async def create_todo(session: AsyncSession, todo_data: TodoCreateSchema, user: User) -> Union[Todo, HTTPException]:
    """
    Создает новую задачу

    Parameters:
        session: асинхронная сессия для работы с базой данных
        todo_data: данные для создания новой задачи
        user: авторизованный пользователь

    Raise:
        HTTPException: недопустимый id статуса задачи

    :return: созданная задача
    """
    data = todo_data.model_dump()
    statuses = await get_statuses(session)
    statuses_ids = [status_obj.id for status_obj in statuses]
    if data["status_id"] not in statuses_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недопустимый id статуса задачи"
        )
    todo = Todo(**todo_data.model_dump())
    todo.user_id = user.id
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    return todo


async def update_todo(session: AsyncSession, todo_id: uuid.UUID,
                      todo_data: TodoUpdateSchema) -> Union[Todo, HTTPException]:
    """
    Обновляет задачу

    Parameters:
        session: асинхронная сессия для работы с базой данных
        todo_id: идентификатор задачи
        todo_data: данные для обновления задачи

    Raise:
        HTTPException: нет данных для обновления

    :return: обновленная задача
    """
    data = {key: value for key, value in todo_data.model_dump().items() if value is not None}
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Необходимо передать хотя бы один параметр для обновления задачи"
        )

    data["modified_date"] = datetime.now()

    stmt = update(Todo).filter(Todo.id == todo_id).values(**data)
    await session.execute(stmt)

    query = select(Todo).filter(Todo.id == todo_id)
    todo = await session.scalar(query)

    return todo


async def delete_todo(session: AsyncSession, todo_id: uuid.UUID) -> Union[dict[str, str], HTTPException]:
    """
    Удаляет задачу

    Parameters:
        session: асинхронная сессия для работы с базой данных
        todo_id: идентификатор задачи

    Raise:
        HTTPException: задача не найдена

    :return: message -> "Задача успешно удалена"
    """
    query = select(Todo).filter(Todo.id == todo_id)
    todo = await session.scalar(query)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )

    await session.delete(todo)

    return {"message": "Задача успешно удалена"}


async def get_report(params: ReportQueryParams, user: User) -> Union[dict[str, str], HTTPException]:
    """
    Возвращает отчёт по задачам

    Parameters:
        user: авторизованный пользователь
        params: query параметры

    Raise:
        HTTPException: неверный формат

    :return: отчёт по задачам
    """
    report_format = params.report_format

    func_map = {
        'csv': get_report_to_csv,
        'xlsx': get_report_to_xlsx
    }
    if report_format not in ('csv', 'xlsx'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Возможные форматы отчета: csv или xlsx. Был запрошен формат - {report_format}"
        )
    file_info = await func_map[report_format](todos=user.todos, user_id=user.id)
    return file_info
