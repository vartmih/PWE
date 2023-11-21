from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = f"{Path(__file__).parent.parent.parent}/.env"


class Settings(BaseSettings):
    """Класс для настройки приложения"""
    SERVER_HOST: str
    SERVER_PORT: int
    DEBUG: bool
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    SECRET: str
    TEST_URL: str

    model_config = SettingsConfigDict(env_file=env_file, env_file_encoding='utf-8', extra='ignore')

    @property
    def db_url(self) -> str:
        """Возвращает URL для подключения к базе данных"""
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def default_db_url(self) -> str:
        """Возвращает URL для подключения к тестовой базе данных"""
        return f'postgresql+asyncpg://postgres:postgres@{self.DB_HOST}:{self.DB_PORT}/postgres'


settings = Settings()
