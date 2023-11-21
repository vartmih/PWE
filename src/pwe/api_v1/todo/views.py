import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from pwe.api_v1.todo import service
from pwe.api_v1.todo.query_params import ReportQueryParams
from pwe.api_v1.todo.schemas import (
    TodoSchema,
    TodoCreateSchema,
    StatusSchema,
    TodoUpdateSchema,
    NoDataExceptionSchema,
    TodoDoesNotExistSchema,
    InvalidReportFormatSchema
)
from pwe.api_v1.user.dependencies import current_active_user
from pwe.api_v1.user.models import User
from pwe.database.db_helper import async_session

router = APIRouter(tags=['Задачи'], prefix='/todos')


@router.get('', response_model=list[TodoSchema])
async def get_todos(user: User = Depends(current_active_user)):
    """Список всех задач"""  # noqa DCO020
    return await service.get_todos(user=user)


@router.post('', response_model=TodoSchema)
async def create_todo(todo_data: TodoCreateSchema, session: Annotated[AsyncSession, Depends(async_session)],
                      user: User = Depends(current_active_user)):
    """Создание новой задачи"""  # noqa DCO020
    return await service.create_todo(session=session, todo_data=todo_data, user=user)


@router.patch('/{todo_id}', response_model=TodoSchema, dependencies=[Depends(current_active_user)],
              responses={400: {"model": NoDataExceptionSchema}})
async def update_todo(todo_id: uuid.UUID, todo_data: TodoUpdateSchema,  # noqa CF009
                      session: Annotated[AsyncSession, Depends(async_session)]):
    """Обновление задачи"""  # noqa DCO020
    return await service.update_todo(session=session, todo_id=todo_id, todo_data=todo_data)


@router.delete('/{todo_id}', dependencies=[Depends(current_active_user)],
               responses={404: {"model": TodoDoesNotExistSchema}})
async def delete_todo(todo_id: uuid.UUID, session: Annotated[AsyncSession, Depends(async_session)]):  # noqa CF009
    """Удаление задачи"""  # noqa DCO020
    return await service.delete_todo(session=session, todo_id=todo_id)


@router.get('/statuses', response_model=list[StatusSchema])
async def get_statuses(session: Annotated[AsyncSession, Depends(async_session)]):
    """Список всех статусов"""  # noqa DCO020
    return await service.get_statuses(session=session)


@router.get('/report', responses={400: {"model": InvalidReportFormatSchema}})
async def get_report(params: ReportQueryParams = Depends(), user: User = Depends(current_active_user)): # noqa CF009
    """Запрос отчета по задачам"""  # noqa DCO020
    file_info = await service.get_report(params=params, user=user)
    return FileResponse(**file_info)
