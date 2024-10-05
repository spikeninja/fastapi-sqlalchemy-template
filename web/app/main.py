import uvicorn
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

    # In dev purposes
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.include_router(auth.router, prefix="/api", tags=["auth"])
    app.include_router(users.router, prefix="/api", tags=["users"])

    container = make_async_container(AppProvider())
    setup_dishka(app=app, container=container)

    return app


app = application_factory()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
