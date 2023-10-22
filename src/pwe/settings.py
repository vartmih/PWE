from pydantic import BaseSettings


class Settings(BaseSettings):
    """Класс для настройки приложения"""
    server_host: str
    server_port: int
    debug: bool
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: str

    def get_db_url(self) -> str:
        """Возвращает URL для подключения к базе данных"""
        return f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'


settings = Settings(
    _env_file=".env",
    _env_file_encoding='utf-8'
)
