from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status

from app.ioc import AppContainer, Scope
from app.repositories import UsersRepository
from app.core.security import decode_access_token, JWTBearer


async def get_users_repo() -> AsyncGenerator[UsersRepository, None]:
    """"""

    async with AppContainer(scope=Scope.REQUEST) as container:
        users_repo = await container.get(UsersRepository)
        yield users_repo


async def get_current_user(
    token: str = Depends(JWTBearer()),
    users_repo: UsersRepository = Depends(get_users_repo),
):
    """Decodes JWT token and extracts user from db"""

    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials are not valid.",
    )

    payload = await decode_access_token(token=token)

    user_id = payload.get("sub", None)
    if not user_id:
        raise cred_exception

    user = await users_repo.get_by_id(_id=int(user_id))
    if not user:
        return cred_exception

    return user
