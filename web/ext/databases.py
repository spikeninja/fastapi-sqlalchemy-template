from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine


class Database:
    def __init__(self, async_engine):
        self.__async_engine: AsyncEngine = async_engine

    def __get_session(self):
        session: AsyncSession = AsyncSession(self.__async_engine)
        session.sync_session.expire_on_commit = False

        return session

    async def fetch_one(self,
                        query,
                        values: dict = None):
        async with self.__get_session() as session:
            async with session.begin():
                result = await session.execute(query, values)
                return result.fetchone()

    async def fetch_all(self,
                        query,
                        values: dict = None):
        async with self.__get_session() as session:
            async with session.begin():
                result = await session.execute(query, values)
                return result.fetchall()

    async def fetch_val(self,
                        query,
                        values,
                        column: Any = 0):
        # need to be fixed
        async with self.__get_session() as session:
            return await session.fetch_val(query, values, column=column)

    async def execute(self,
                      query):
        async with self.__get_session() as session:
            async with session.begin():
                result = await session.execute(query)
                return result
