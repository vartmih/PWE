from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .dependencies import get_db_settings

db_settings = get_db_settings()

DATABASE_URL = f"postgresql://{db_settings.username}:{db_settings.password}@" \
               f"{db_settings.host}:{db_settings.port}/{db_settings.db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Model = declarative_base()
