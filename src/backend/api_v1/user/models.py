from datetime import datetime
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.api_v1.todo.models import Todo


class User(SQLAlchemyBaseUserTableUUID, Base):
    """Модель пользователя"""
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    birth_date: Mapped[datetime] = mapped_column(nullable=True)
    date_joined: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_login: Mapped[datetime] = mapped_column(nullable=True)

    todos: Mapped[list['Todo']] = relationship(back_populates="user", lazy='joined')
