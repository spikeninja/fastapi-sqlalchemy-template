from datetime import datetime, timedelta

import jwt
import bcrypt

from app.core.config import load_config

settings = load_config()


async def hash_password(password: str) -> str:
    """Async wrapper for bcrypt operation"""

    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def verify_password(password: str, hashed: str) -> bool:
    """"""

    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


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
        algorithms=[settings.algorithm],
    )
