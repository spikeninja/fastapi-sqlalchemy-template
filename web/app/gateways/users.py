from typing import Any
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.users import User
from app.db.tables import users_table
from app.utils.functions import utcnow
from app.core.security import hash_password


class UsersGateway:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _map_user(self, row: Any) -> User:
        return User(
            id=row.id,
            name=row.name,
            email=row.email,
            hashed_password=row.hashed_password,
            created_at=row.created_at,
            updated_at=row.updated_at,
            deleted_at=row.deleted_at,
        )

    async def create(
        self,
        name: str,
        email: str,
        password: str,
    ) -> User:
        """"""

        hashed_password = await hash_password(password=password)

        user = User(
            id=uuid4(),
            name=name,
            email=email,
            created_at=utcnow(),
            updated_at=utcnow(),
            deleted_at=None,
            hashed_password=hashed_password,
        )

        self.session.add(user)

        return user

    async def get_by_id(self, _id: int) -> User | None:
        """"""

        query = sa.select(users_table).where(users_table.c.id == _id)
        result = await self.session.execute(query)
        row = result.fetchone()
        if not row:
            return None

        return self._map_user(row)

    async def get_by_email(self, email: str) -> User | None:
        """"""

        query = sa.select(users_table).where(users_table.c.email == email)

        row = await self.session.scalar(query)
        if not row:
            return None

        return self._map_user(row)

    async def get_all(
        self,
        limit: int | None,
        offset: int | None,
    ):
        """"""

        query = sa.select(users_table).limit(limit).offset(offset)
        results = await self.session.execute(query)

        return [self._map_user(row) for row in results.fetchall()]

    async def update(self, _id: int, values: dict):
        """"""

        query = (
            sa.update(users_table)
            .where(users_table.c.id == _id)
            .values(
                {
                    **values,
                    users_table.c.updated_at: utcnow(),
                }
            )
        )

        await self.session.execute(query)
        await self.session.commit()

    async def delete(self, _id: int):
        """Deletes a user by their id"""

        query = (
            sa.update(users_table)
            .values({users_table.c.deleted_at: utcnow()})
            .where(users_table.c.id == _id)
        )

        await self.session.execute(query)
        await self.session.commit()
