from typing import AsyncGenerator
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status

from app.ioc import AppContainer, Scope
from app.gateways.users import UsersGateway
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_users_repo() -> AsyncGenerator[UsersGateway, None]:
    """"""

    async with AppContainer(scope=Scope.REQUEST) as container:
        users_repo = await container.get(UsersGateway)
        yield users_repo


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    users_repo: UsersGateway = Depends(get_users_repo),
):
    """Decodes JWT token and extracts user from db"""

    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials are not valid.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = await decode_access_token(token=token)
        user_id = payload.get("sub")
        if not user_id:
            raise cred_exception
    except InvalidTokenError:
        raise cred_exception

    user = await users_repo.get_by_id(_id=int(user_id))
    if not user:
        raise cred_exception

    return user
