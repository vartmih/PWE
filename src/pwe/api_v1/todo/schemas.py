import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class StatusBaseSchema(BaseModel):
    """Схема для статусов todo-задач"""
    status_name: str

    class ConfigDict:
        """Конфигурация схемы"""
        from_attributes = True


class StatusCreateSchema(StatusBaseSchema):
    """Расширенная схема для статусов todo-задач"""
    id: uuid.UUID


class TodoBaseSchema(BaseModel):
    """Схема для todo-задач"""
    todo: str
    status_id: uuid.UUID


class TodoSchema(TodoBaseSchema):
    """Расширенная схема для todo-задач"""
    id: uuid.UUID
    created_date: datetime
    modified_date: datetime | None
    author: EmailStr
    status: str

    class ConfigDict:
        """Конфигурация схемы"""
        from_attributes = True


class TodoCreateSchema(TodoBaseSchema):
    """Схема для создания todo-задач"""
    pass
