from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from pwe.api_v1.todo import service
from pwe.api_v1.todo.schemas import TodoSchema, TodoCreateSchema, StatusCreateSchema
from pwe.api_v1.user.dependencies import current_active_user
from pwe.api_v1.user.models import User
from pwe.database.db_helper import async_session

router = APIRouter(tags=['Задачи'], prefix='/todos')


@router.get('', response_model=list[TodoSchema])
async def get_todos(user: User = Depends(current_active_user)):
    """Список всех задач"""  # noqa DCO020
    return await service.get_todos(user)


@router.post('', response_model=TodoSchema)
async def create_todo(todo_data: TodoCreateSchema, session: Annotated[AsyncSession, Depends(async_session)],
                      user: User = Depends(current_active_user)):
    """Создание новой задачи"""  # noqa DCO020
    return await service.create_todo(session, todo_data, user)


@router.get('/statuses', response_model=list[StatusCreateSchema])
async def get_statuses(session: Annotated[AsyncSession, Depends(async_session)]):
    """Список всех статусов"""  # noqa DCO020
    return await service.get_statuses(session)
