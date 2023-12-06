from collections.abc import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from backend.settings import settings
from backend.utils import get_alembic_config_from_db_url


class DatabaseHelper:
    """Класс для работы с базой данных"""

    def __init__(self, db_url: str, echo: bool) -> None:
        """
        Инициализация класса

        Parameters:
            db_url: URL для подключения к базе данных
            echo: режим отладки

        :return: None
        """
        self.engine = create_async_engine(db_url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False
        )
        self.alembic_config = get_alembic_config_from_db_url(db_url)

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Генератор сессий

        yield: сессия

        Raise:
            SQLAlchemyError: если произошла ошибка при подключении или при работе с базой данных
        """
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError as error:
                await session.rollback()
                raise SQLAlchemyError(error)


db_helper = DatabaseHelper(db_url=settings.db_url, echo=settings.DEBUG)
async_session = db_helper.session_dependency
