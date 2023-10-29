import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import ForeignKey, String, text
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from sqlalchemy.orm import Mapped, relationship, mapped_column

from ...database import Base

if TYPE_CHECKING:
    from ..user.models import User


class Todo(Base):
    """Модель для todo-задач"""
    __tablename__ = 'todo'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    todo: Mapped[str] = mapped_column(String(150))
    modified_date: Mapped[datetime | None]
    status_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('status.id', ondelete='CASCADE', onupdate='CASCADE'))
    created_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))

    status_obj: Mapped['Status'] = relationship(back_populates='todos', viewonly=True, lazy='joined')
    status: AssociationProxy[str] = association_proxy("status_obj", "status_name")
    user: Mapped['User'] = relationship(back_populates='todos', viewonly=True, lazy='joined')
    author: AssociationProxy[EmailStr] = association_proxy("user", "email")


class Status(Base):
    """Модель для статусов todo-задач"""
    __tablename__ = 'status'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4,
                                          server_default=text("gen_random_uuid()"))
    status_name: Mapped[str]
    todos: Mapped[list['Todo']] = relationship(back_populates='status_obj')
