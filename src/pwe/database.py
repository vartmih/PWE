from asyncio import current_task
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, async_scoped_session

from pwe.settings import settings


class DatabaseHelper:
    """Класс для работы с базой данных"""

    def __init__(self, db_url: str, debug: bool) -> None:
        """
        Инициализация класса

        Parameters:
            db_url: URL для подключения к базе данных
            debug: режим отладки

        :return: None
        """
        self.engine = create_async_engine(db_url, echo=debug)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False
        )

    def get_scoped_session(self):
        """Возвращает сессию для работы с базой данных"""
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return session

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Генератор сессий

        yield: сессия
        """
        with self.get_scoped_session() as session:
            yield session
            await session.remove()


db_helper = DatabaseHelper(
    db_url=settings.get_db_url(),
    debug=settings.debug
)
