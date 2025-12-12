from typing import AsyncIterable

from redis.asyncio import Redis as AsyncRedis
from dishka import provide, Provider, Scope, make_async_container
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.core.config import Config
from app.gateways import gateways
from app.services.filte_storage import S3FilesStorage


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def config(self) -> Config:
        return Config.from_env()

    @provide(scope=Scope.APP)
    async def redis(self, config: Config) -> AsyncIterable[AsyncRedis]:
        """"""
        client = AsyncRedis.from_url(
            url=config.cache_url,
            encoding="utf-8",
            decode_responses=True,
        )
        yield client
        await client.aclose()

    @provide(scope=Scope.APP)
    async def get_engine(self, config: Config) -> AsyncIterable[AsyncEngine]:
        """"""
        engine = create_async_engine(
            future=True,
            pool_size=40,
            url=config.async_postgresql_url,
        )
        try:
            yield engine
        finally:
            await engine.dispose()

    @provide(scope=Scope.APP)
    def get_session_maker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        """"""
        return async_sessionmaker(
            engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        """"""
        async with session_maker() as session:
            yield session

    gateways = provide(*gateways, scope=Scope.REQUEST)
    s3_file_storage = provide(S3FilesStorage, scope=Scope.APP)


class TestProvider(Provider):
    @provide(scope=Scope.APP)
    def config(self) -> Config:
        return Config.from_env()

    @provide(scope=Scope.APP)
    async def redis(self, config: Config) -> AsyncIterable[AsyncRedis]:
        """"""
        client = AsyncRedis.from_url(
            url=config.cache_url,
            encoding="utf-8",
            decode_responses=True,
        )
        yield client
        await client.aclose()

    @provide(scope=Scope.APP)
    async def get_engine(self, config: Config) -> AsyncIterable[AsyncEngine]:
        """"""
        engine = create_async_engine(
            future=True,
            pool_size=40,
            url=config.async_postgresql_url,
        )
        try:
            yield engine
        finally:
            await engine.dispose()

    @provide(scope=Scope.APP)
    def get_session_maker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        """"""
        return async_sessionmaker(
            engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        """"""
        async with session_maker() as session:
            yield session

    gateways = provide(*gateways, scope=Scope.REQUEST)
    s3_file_storage = provide(S3FilesStorage, scope=Scope.APP)


AppContainer = make_async_container(AppProvider())
