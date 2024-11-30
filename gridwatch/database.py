from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from gridwatch.settings import app_settings

DATABASE_URL = f"postgresql+asyncpg://{app_settings.db_user}:{app_settings.db_password}@{app_settings.db_host}:{app_settings.db_port}/{app_settings.db_name}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
