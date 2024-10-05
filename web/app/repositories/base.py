from app.db.resources import AsyncSession


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
