from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str
    server_port: int


class DBSettings(BaseSettings):
    username: str
    password: str
    db_name: str
    host: str
    port: str

    class Config:
        env_prefix = 'POSTGRES_'
        env_file = '.env'


settings = Settings(
    _env_file=".env",
    _env_file_encoding='utf-8'
)
