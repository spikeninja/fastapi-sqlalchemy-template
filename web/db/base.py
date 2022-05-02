from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine

from core import config
from ext.databases import Database


SQLALCHEMY_DATABASE_URL = \
    f"postgresql+asyncpg://{config.PG_USER}:{config.PG_PASS}@{config.PG_HOST}/{config.DATABASE}"

metadata = MetaData()

__async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    future=True
)

database = Database(__async_engine)
