from fastapi import Depends, HTTPException, status

from db.base import database
from repositories.users import UserRepository
from core.security import decode_access_token, JWTBearer


def get_user_repository():
    return UserRepository(database)


async def get_current_user(
        users: UserRepository = Depends(get_user_repository),
        token: str = Depends(JWTBearer())):
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                   detail="Credentials are not valid.")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get("sub")
    if email is None:
        raise cred_exception
    user = await users.get_by_email(email=email)
    if user is None:
        return cred_exception
    return user


