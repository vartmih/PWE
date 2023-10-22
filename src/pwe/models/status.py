import uuid
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .todo import Todo


class Status(Base):
    """Модель для статусов todo-задач"""
    __tablename__ = 'status'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    status_name: Mapped[str]
    todos: Mapped[list['Todo']] = relationship(back_populates='status')
