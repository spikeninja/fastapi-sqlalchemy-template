from app.db.resources import AsyncSession
from app.repositories.users import UsersRepository


class Repositories:
    def __init__(self, session: AsyncSession):
        self.session = session

    def users(self) -> UsersRepository:
        return UsersRepository(session=self.session)
