from typing import AsyncGenerator

from loguru import logger
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession

from app.core.config import settings

Base = declarative_base()


class DatabaseManager:
    @classmethod
    async def create_sa_engine(cls) -> AsyncGenerator[AsyncEngine, None]:
        logger.debug("Initializing SQLAlchemy engine")
        engine = create_async_engine(
            future=True,
            pool_size=35,
            json_serializer=lambda x: x,
            url=settings.async_postgresql_url,
        )
        logger.debug("SQLAlchemy engine has been initialized")
        try:
            yield engine
        finally:
            await engine.dispose()
            logger.debug("SQLAlchemy engine has been cleaned up")

    @classmethod
    async def create_session(cls, engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
        logger.debug("SESSION 1: INITIATING")
        async with AsyncSession(engine, expire_on_commit=False, autoflush=False) as session:
            logger.debug("SESSION 2: INITIATED")
            yield session
        logger.debug("SESSION 3: CLOSED")
