from dishka import provide, Provider, Scope, make_async_container

from app.repositories import Repositories
from app.db.resources import DatabaseManager


class AppProvider(Provider):
    engine = provide(DatabaseManager.create_sa_engine, scope=Scope.APP)
    session = provide(DatabaseManager.create_session, scope=Scope.REQUEST)

    repositories = provide(Repositories, scope=Scope.REQUEST)


AppContainer = make_async_container(AppProvider())
