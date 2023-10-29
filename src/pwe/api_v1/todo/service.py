from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..todo.models import Todo, Status
from ..todo.schemas import TodoCreateSchema
from ..user.models import User


async def get_todos(user: User) -> list[Todo | None]:
    """
    Возвращает список всех задач

    Parameters:
        user: авторизованный пользователь

    :return: список всех задач
    """
    return user.todos


async def create_todo(session: AsyncSession, todo_data: TodoCreateSchema, user: User) -> Todo:
    """
    Создает новую задачу

    Parameters:
        session: асинхронная сессия для работы с базой данных
        todo_data: данные для создания новой задачи
        user: авторизованный пользователь

    :return: созданная задача
    """
    todo = Todo(**todo_data.dict())
    todo.user_id = user.id
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    return todo


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
