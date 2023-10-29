from datetime import datetime
from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped, relationship

from ...database import Base, db_helper

if TYPE_CHECKING:
    from ..todo.models import Todo


class User(SQLAlchemyBaseUserTableUUID, Base):
    """Модель пользователя"""
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    birth_date: Mapped[datetime] = mapped_column(nullable=True)
    date_joined: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_login: Mapped[datetime] = mapped_column(nullable=True)

    todos: Mapped[list['Todo']] = relationship(back_populates="user", lazy='joined')


async def get_user_db(session: AsyncSession = Depends(db_helper.get_scoped_session)):
    """
    Возвращает адаптер для работы с базой данных

    Parameters:
        session: асинхронная сессия для работы с базой данных

    yields:
        SQLAlchemyUserDatabase: адаптер
    """
    yield SQLAlchemyUserDatabase(session, User)
