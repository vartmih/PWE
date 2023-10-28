import datetime
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from pwe.models import Base

if TYPE_CHECKING:
    from src.pwe.models import Todo


class User(SQLAlchemyBaseUserTableUUID, Base):
    """Модель пользователя"""
    username: Mapped[str] = mapped_column(String(50), unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    birth_date: Mapped[datetime.date] = mapped_column(nullable=True)

    todos: Mapped[list['Todo']] = relationship(back_populates="user", lazy='joined')
