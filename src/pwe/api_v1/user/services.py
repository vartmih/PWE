from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from pwe.api_v1.user.models import User
from pwe.database.db_helper import db_helper


async def get_user_db(session: AsyncSession = Depends(db_helper.session_dependency)):
    """
    Возвращает адаптер для работы с базой данных

    Parameters:
        session: асинхронная сессия для работы с базой данных

    yields:
        SQLAlchemyUserDatabase: адаптер
    """
    yield SQLAlchemyUserDatabase(session=session, user_table=User)
