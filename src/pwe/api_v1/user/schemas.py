import datetime
import uuid
from typing import Optional

from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    """Базовая схема пользователя"""
    email: EmailStr
    first_name: str
    last_name: str
    birth_date: datetime.date

    class Config:
        """Конфигурация схемы"""
        orm_mode = True


class UserSchema(BaseUser, UserBaseSchema):
    """Расширенная схема пользователя"""
    id: uuid.UUID


class UserCreateSchema(UserBaseSchema, BaseUserCreate):
    """Схема для регистрации нового пользователя"""
    pass


class UserUpdateSchema(BaseUserUpdate):
    """Схема для обновления пользователя"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[str] = None
