import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .status import Status
    from ..api_v1.user.models import User


class Todo(Base):
    """Модель для todo-задач"""
    __tablename__ = 'todo'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    todo: Mapped[str] = mapped_column(String(150))
    modified_date: Mapped[datetime | None]
    status_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('status.id', ondelete='CASCADE', onupdate='CASCADE'))
    created_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))

    status: Mapped['Status'] = relationship(back_populates='todos', lazy='joined')
    user: Mapped['User'] = relationship(back_populates='todos', lazy='joined')
