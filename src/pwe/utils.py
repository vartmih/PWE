import os
from pathlib import Path

import pkg_resources
from alembic.config import Config
import toml

from pwe.settings import settings


def get_alembic_config_from_db_url(db_url: str | None = None) -> Config:
    """
    Устанавливает URL для подключения к базе данных для Alembic

    Parameters:
        db_url: URL для подключения к базе данных

    :return: Конфигурация для Alembic
    """
    root_path = Path(__file__).parent.parent.parent
    alembic_config_path = root_path / 'alembic.ini'

    config = Config(alembic_config_path)
    alembic_location = config.get_main_option('script_location')

    if not os.path.isabs(alembic_location):
        config.set_main_option('script_location', str(root_path / alembic_location))

    if db_url is None:
        db_url = settings.db_url

    config.set_main_option('sqlalchemy.url', db_url)

    return config


def get_app_info() -> dict[str, str]:
    """
    Возвращает информацию об используемых пакетах и их версиях
    :return: словарь с названиями пакетов и их версиями, если это питоновские пакеты
    """
    packages = (
        'pwe',
        'fastapi',
        'sqlalchemy',
        'pydantic',
        'alembic',
        'pytest',
        'pytest-asyncio',
        'fastapi-users',
        'uvicorn',
        'asyncpg',
        'python=3.10',
        'postgresql=15.4',
        'docker',
        'docker-compose',
    )
    app_info = {}
    for package in packages:
        try:
            app_info[package] = pkg_resources.get_distribution(package).version
        except Exception:  # noqa
            app_info[package] = 'unknown'
    return app_info


def get_version_app() -> str:
    """
    Получение версии приложения из pyproject.toml
    :return: версия приложения
    """
    application = toml.load(
        Path(__file__).parent.parent.parent / "pyproject.toml")

    return application["tool"]["poetry"]["version"]
