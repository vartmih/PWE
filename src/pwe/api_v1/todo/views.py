from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from pwe.api_v1.todo import service
from pwe.api_v1.todo.schemas import TodoSchema, TodoCreateSchema, StatusCreateSchema, StatusBaseSchema
from pwe.database import db_helper

router = APIRouter(tags=['Задачи'], prefix='/todo')


@router.get('/', response_model=list[TodoSchema])
async def get_todos(session: AsyncSession = Depends(db_helper.get_scoped_session)):
    """Возвращает список всех задач""" # noqa DCO020
    return await service.get_todos(session)


@router.post('/', response_model=TodoSchema)
async def create_todo(todo_data: TodoCreateSchema, session: AsyncSession = Depends(db_helper.get_scoped_session)):
    """Создание новой задачи""" # noqa DCO020
    return await service.create_todo(session, todo_data)


@router.post('/status', response_model=StatusCreateSchema)
async def create_status(status_data: StatusBaseSchema, session: AsyncSession = Depends(db_helper.get_scoped_session)):
    """Создание нового статуса""" # noqa DCO020
    return await service.create_status(session, status_data)


@router.get('/status', response_model=list[StatusCreateSchema])
async def get_statuses(session: AsyncSession = Depends(db_helper.get_scoped_session)):
    """Возвращает список всех статусов""" # noqa DCO020
    return await service.get_statuses(session)
