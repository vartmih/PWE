import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class StatusSchema(BaseModel):
    """Схема для статусов todo-задач"""
    status_name: str
    id: uuid.UUID

    class ConfigDict:
        """Конфигурация схемы"""
        from_attributes = True


class TodoBaseSchema(BaseModel):
    """Схема для todo-задач"""
    todo: str
    status: str


class TodoSchema(TodoBaseSchema):
    """Расширенная схема для todo-задач"""
    id: uuid.UUID
    created_date: datetime
    modified_date: datetime | None
    author: EmailStr

    class ConfigDict:
        """Конфигурация схемы"""
        from_attributes = True


class TodoCreateSchema(BaseModel):
    """Схема для создания todo-задач"""
    todo: str
    status_id: uuid.UUID


class TodoUpdateSchema(BaseModel):
    """Схема для обновления todo-задач"""
    todo: str | None = None
    status_id: uuid.UUID | None = None


class NoDataExceptionSchema(BaseModel):
    """Схема для 400 статуса - нет данных для обновления"""
    detail: str = 'Необходимо передать хотя бы один параметр для обновления задачи'


class TodoDoesNotExistSchema(BaseModel):
    """Схема для 404 статуса - Задача не найдена"""
    detail: str = 'Задача не найдена'


class InvalidReportFormatSchema(BaseModel):
    """Схема для 400 статуса - неверный формат отчета"""
    detail: str = 'Возможные форматы отчета: csv или xlsx. Был запрошен формат - {report_format}'


class StatusDoesNotExistSchema(BaseModel):
    """Схема для 400 статуса - недопустимый id статуса задачи"""
    detail: str = 'Недопустимый id статуса задачи'
