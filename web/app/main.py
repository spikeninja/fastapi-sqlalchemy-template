from fastapi import FastAPI
from dishka import make_async_container
from fastapi.middleware.cors import CORSMiddleware
from dishka.integrations.fastapi import setup_dishka

from app.api import auth, users
from app.ioc import AppProvider
from app.utils.fastapi import lifespan


def application_factory() -> FastAPI:
    """"""

    app = FastAPI(lifespan=lifespan)

    # todo: dev only
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.include_router(auth.router, prefix="/api", tags=["auth"])
    app.include_router(users.router, prefix="/api", tags=["users"])

    return app


def setup_app():
    """"""
    app_ = application_factory()

    container = make_async_container(AppProvider())
    setup_dishka(app=app_, container=container)

    return app_


app = application_factory()
