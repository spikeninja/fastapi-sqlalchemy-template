import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from testcontainers.redis import RedisContainer
from testcontainers.postgres import PostgresContainer
from dishka.integrations.fastapi import setup_dishka
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from dishka import make_async_container, AsyncContainer, Scope

from app.ioc import TestProvider
from app.utils.functions import utcnow
from app.utils.fastapi import lifespan
from app.schemas.users import UserDTO
from app.db.base import MAPPER_REGISTRY
from app.main import application_factory
from app.api.dependencies import get_current_user
from app.core.config import load_config, Config


@pytest.fixture(scope="session")
def redis_container(request):
    """"""
    with RedisContainer("redis:7-alpine") as redis_:
        yield redis_


@pytest.fixture(scope="session")
def postgres_container(request):
    """"""
    settings = load_config()
    with PostgresContainer(
        image="postgres:16-alpine",
        password=settings.pg_pass,
        username=settings.pg_user,
        dbname=settings.database,
        port=settings.pg_port,
        driver="psycopg",
    ) as postgres:
        yield postgres


@pytest.fixture(scope="session")
def config(postgres_container, redis_container):
    pg_host = postgres_container.get_container_host_ip()
    pg_port = postgres_container.get_exposed_port(int(os.environ["POSTGRES_PORT"]))

    redis_host = redis_container.get_container_host_ip()
    redis_port = redis_container.get_exposed_port(int(os.environ["REDIS_PORT"]))

    os.environ["REDIS_HOST"] = redis_host
    os.environ["REDIS_PORT"] = str(redis_port)

    os.environ["POSTGRES_HOST"] = pg_host
    os.environ["POSTGRES_PORT"] = str(pg_port)

    return load_config()


@pytest_asyncio.fixture(loop_scope="session", scope="session")
async def container(config: Config) -> AsyncGenerator[AsyncContainer, None]:
    """"""
    container = make_async_container(TestProvider())

    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        await conn.run_sync(MAPPER_REGISTRY.metadata.create_all)

    yield container
    await container.close()


@pytest_asyncio.fixture(loop_scope="session", scope="function")
async def session(container: AsyncContainer) -> AsyncGenerator[AsyncSession, None]:
    async with container(scope=Scope.REQUEST) as container_:
        session = await container_.get(AsyncSession)
        yield session


@pytest_asyncio.fixture(loop_scope="session", scope="function")
async def test_client(container: AsyncContainer) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client that uses the override_get_db fixture to return a session."""

    async def test_get_current_user() -> UserDTO:
        """"""
        return UserDTO(
            id=1,
            deleted_at=None,
            updated_at=utcnow(),
            created_at=utcnow(),
            name="John",
            email="user@example.com",
            hashed_password="supersecretandhashed",
        )

    app = application_factory()
    app.dependency_overrides[get_current_user] = test_get_current_user
    setup_dishka(container, app)

    async with lifespan(app=app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            yield ac
