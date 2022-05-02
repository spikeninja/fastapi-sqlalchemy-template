import datetime

from typing import List, Optional

from db.users import users
from models.users import User, UserIn
from core.security import hash_password
from repositories.base import BaseRepository


class UserRepository(BaseRepository):

    async def get_all(self,
                      limit: int = 100,
                      skip: int = 0) -> List[User]:
        query = users.select().limit(limit).offset(skip)
        return [
            User.parse_obj(obj)
            for obj in await self.database.fetch_all(query=query)
        ]

    async def get_by_id(self, id: int) -> Optional[User]:
        query = users.select().where(users.c.id==id)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def get_by_email(self, email: str) -> Optional[User]:
        query = users.select().where(users.c.email==email)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create(self, u: UserIn) -> User:
        user = User(
            id=0,
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            created_at=datetime.datetime.utcnow(),
            updated_at = datetime.datetime.utcnow()
        )

        values = {**user.dict()}
        values.pop("id", None)

        query = users.insert().values(**values)
        result = await self.database.execute(query)

        user.id = result.inserted_primary_key[0]

        return user

    async def update(self, id: int, u: UserIn) -> User:
        user = User(
            id=id,
            name=u.name,
            email=u.email,
            hashed_password=u.password2,
            created_at=datetime.datetime.utcnow(),
            updated_at = datetime.datetime.utcnow()
        )

        values = {**user.dict()}
        values.pop("created_at", None)
        values.pop("id", None)
        query = users.update().where(users.c.id==id).values(**values)
        await self.database.execute(query)

        return user

