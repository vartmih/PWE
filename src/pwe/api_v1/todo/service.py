from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from pwe.api_v1.todo.schemas import TodoCreateSchema, StatusBaseSchema
from pwe.models import Todo, Status


async def get_todos(session: AsyncSession) -> list[Todo | None]:
    """
    Возвращает список всех задач

    Parameters:
        session: асинхронная сессия для работы с базой данных

    :return: список всех задач
    """
    todos_query = select(Todo).options(selectinload(Todo.status))
    todos = await session.scalars(todos_query)
    return list(todos)


async def create_todo(session: AsyncSession, todo_data: TodoCreateSchema) -> Todo:
    """
    Создает новую задачу

    Parameters:
        session: асинхронная сессия для работы с базой данных
        todo_data: данные для создания новой задачи

    :return: созданная задача
    """
    todo = Todo(**todo_data.dict())
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    return todo


async def create_status(session: AsyncSession, status_data: StatusBaseSchema) -> Status:
    """
    Создает новый статус

    Parameters:
        session: асинхронная сессия для работы с базой данных
        status_data: данные для создания нового статуса

    :return: созданный статус
    """
    status = Status(**status_data.dict())
    session.add(status)
    await session.commit()
    return status


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
