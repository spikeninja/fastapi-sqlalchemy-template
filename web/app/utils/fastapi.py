from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.resources import DatabaseManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """"""
    engine = await DatabaseManager.create_sa_engine().__anext__()
    yield
    await engine.dispose()
