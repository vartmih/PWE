from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from pwe.api_v1.todo import service
from pwe.api_v1.todo.schemas import TodoSchema, TodoCreateSchema, StatusCreateSchema
from pwe.api_v1.user.models import User
from pwe.api_v1.user.views import fastapi_users
from pwe.database import db_helper

router = APIRouter(tags=['Задачи'], prefix='/todo')

current_active_user = fastapi_users.current_user(active=True)


@router.get('/', response_model=list[TodoSchema])
async def get_todos(user: User = Depends(current_active_user)):
    """Возвращает список всех задач"""  # noqa DCO020
    return await service.get_todos(user)


@router.post('/', response_model=TodoSchema)
async def create_todo(todo_data: TodoCreateSchema, session: AsyncSession = Depends(db_helper.get_scoped_session),
                      user: User = Depends(current_active_user)):
    """Создание новой задачи"""  # noqa DCO020
    return await service.create_todo(session, todo_data, user)


@router.get('/status', response_model=list[StatusCreateSchema])
async def get_statuses(session: AsyncSession = Depends(db_helper.get_scoped_session)):
    """Возвращает список всех статусов"""  # noqa DCO020
    return await service.get_statuses(session)
