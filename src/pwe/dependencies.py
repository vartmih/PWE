from functools import lru_cache

from sqlalchemy.orm import Session

from pwe import database
from pwe import settings


def get_db() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache
def get_db_settings() -> settings.DBSettings:
    return settings.DBSettings()