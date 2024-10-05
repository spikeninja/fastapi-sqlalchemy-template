from datetime import datetime

import sqlalchemy as sa

from app.db.models import UsersModel
from app.core.security import hash_password
from app.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    async def create(self, name: str, email: str, password: str) -> UsersModel:
        """Creates a new user"""

        hashed_password = await hash_password(password=password)

        user = UsersModel(
            name=name,
            email=email,
            hashed_password=hashed_password,
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.flush(user)

        return user

    async def get_by_id(self, _id: int) -> UsersModel | None:
        """Returns a user by their id"""

        query = sa.select(UsersModel).where(UsersModel.id == _id)

        return await self.session.scalar(query)

    async def get_by_email(self, email: str) -> UsersModel:
        """Return a user by their email"""

        query = sa.select(UsersModel).where(UsersModel.email == email)

        return await self.session.scalar(query)

    async def get_all(self, limit: int | None, offset: int | None) -> list[UsersModel]:
        """Returns all users"""

        query = (
            sa.select(UsersModel)
            .limit(limit)
            .offset(offset)
        )

        return list(await self.session.scalars(query))

    async def update(self, _id: int, values: dict):
        """Updates a user by their id"""

        now_ = datetime.utcnow()

        query = (
            sa.update(UsersModel)
            .where(UsersModel.id == _id)
            .values({
                **values,
                UsersModel.updated_at: now_,
            })
        )

        await self.session.execute(query)
        await self.session.commit()

    async def delete(self, _id: int):
        """Deletes a user by their id"""

        now_ = datetime.utcnow()

        query = (
            sa.update(UsersModel)
            .values({UsersModel.deleted_at: now_})
            .where(UsersModel.id == _id)
        )

        await self.session.execute(query)
        await self.session.commit()
