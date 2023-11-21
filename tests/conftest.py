import asyncio
from datetime import datetime
from http.cookiejar import CookieJar

import pytest
from alembic.config import Config
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from pwe.database.db_helper import DatabaseHelper, async_session
from pwe.main import app
from pwe.settings import settings
from pwe.utils import get_alembic_config_from_db_url
from tests.user.test_user import TestUser

DATE = datetime.now().strftime("%d_%m_%Y")
DB_URL = f'{settings.db_url}_test_{DATE}'

DB_HELPER = DatabaseHelper(DB_URL, echo=True)


@pytest.fixture(scope="session", autouse=True)
async def create_test_database():
    """
    Создает тестовую базу данных и удаляет ее после завершения теста.
    """
    db_name = DB_URL.split('/')[-1]

    # Подключаемся к дефолтной базе данных для создания тестовой базы данных
    engine = create_async_engine(settings.default_db_url, isolation_level="AUTOCOMMIT")
    async with engine.begin() as conn:
        query = f"CREATE DATABASE {db_name}"
        await conn.execute(text(query))
    yield  # Выполнение тестов
    async with engine.begin() as conn:
        query = f"DROP DATABASE {db_name} WITH (FORCE)"
        await conn.execute(text(query))


@pytest.fixture
def alembic_config() -> Config:
    """
    Фикстура для получения конфигурации Alembic, привязанной к тестовой базе данных.
    """
    return get_alembic_config_from_db_url(DB_URL)


@pytest.fixture(scope="session")
def event_loop():
    """Переопределение событийного цикла для расшаривания области видимости на всю сессию"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def override_async_session():
    """
    Функция для подмены сессии в зависимостях

    Yields:
        session: сессия для работы с базой данных
    """
    async with DB_HELPER.session_factory() as session:
        yield session
        await session.commit()


#  Подменяем зависимость на сессию с подключением к тестовой базе данных
app.dependency_overrides[async_session] = override_async_session


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    """
    Фикстура получения асинхронного клиента для тестирования API
    Yields:
        client: асинхронный клиент
    """
    async with AsyncClient(app=app, base_url=settings.TEST_URL) as client:
        yield client


@pytest.fixture(scope="session")
async def cookie(client: AsyncClient) -> CookieJar:
    user_data = TestUser.user_data_for_cookie
    await client.post("/users/register", json=user_data)
    login_response = await client.post(
        url="/users/login",
        data={
            "username": user_data['email'],
            "password": user_data['password']
        })
    cookie = login_response.cookies.jar
    return cookie
