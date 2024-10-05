from datetime import datetime, timedelta

import jwt
import bcrypt
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings


async def hash_password(password: str) -> str:
    """Async wrapper for bcrypt operation"""

    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')


async def verify_password(password: str, hashed: str) -> bool:
    """"""

    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed.encode("utf-8")
    )


async def create_access_token(minutes: int, payload: dict) -> str:
    """"""

    to_encode = payload.copy()

    exp = datetime.utcnow() + timedelta(minutes=minutes)
    to_encode.update({"exp": exp})

    return jwt.encode(
        payload=to_encode,
        key=settings.secret_key,
        algorithm=settings.algorithm,
    )


async def decode_access_token(token: str) -> dict:
    """"""

    return jwt.decode(
        jwt=token,
        key=settings.secret_key,
        algorithms=[settings.algorithm]
    )


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        exp = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid auth token."
        )

        if credentials:
            try:
                token = await decode_access_token(token=credentials.credentials)
            except jwt.PyJWTError as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"{e}"
                )

            if token is None:
                raise exp

            return credentials.credentials

        else:
            raise exp
