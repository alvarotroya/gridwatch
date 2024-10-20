from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from gridwatch.settings import app_settings

DATABASE_URL = f"postgresql://{app_settings.db_user}:{app_settings.db_password}@localhost:{app_settings.db_port}/{app_settings.db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_tables_if_not_existent():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
