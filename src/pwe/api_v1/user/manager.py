import uuid
from datetime import datetime
from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, UUIDIDMixin, InvalidPasswordException

from pwe.api_v1.user.models import User, get_user_db
from pwe.api_v1.user.schemas import UserCreateSchema
from pwe.settings import settings


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """Менеджер пользователей"""
    reset_password_token_secret = settings.secret
    verification_token_secret = settings.secret

    async def on_after_login(
            self,
            user: User,
            request: Optional[Request] = None,
            response: Optional[Response] = None,
    ) -> None:
        """
        Проставляет дату последнего входа пользователя в систему

        Parameters:
            user: модель пользователя
            request: запрос
            response: ответ

        :return: None
        """
        user.last_login = datetime.utcnow()
        await self.user_db.session.commit()
        print(f"Пользователь {user.id} вошел в систему.")

    async def validate_password(self, password: str, user: UserCreateSchema | User) -> None:
        """
        Валидация пароля

        Parameters:
            password: пароль
            user: модель пользователя

        Raises:
            InvalidPasswordException: если пароль содержит адрес электронной почты или его длина меньше 8 символов
        :return: None
        """
        if len(password) < 8:
            raise InvalidPasswordException(reason="Пароль должен быть не менее 8 символов")
        if user.email in password:
            raise InvalidPasswordException(reason="Пароль не должен содержать адрес электронной почты")


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Возвращает экземпляр UserManager

    Parameters:
        user_db: адаптер для работы с базой данных

    yields:
        UserManager: менеджер пользователей
    """
    yield UserManager(user_db)
