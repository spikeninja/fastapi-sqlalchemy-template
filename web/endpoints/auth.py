from fastapi import APIRouter, Depends, HTTPException, status

from models.token import Login, Token
from repositories.users import UserRepository
from endpoints.depends import get_user_repository
from core.security import create_access_token, verify_password


router = APIRouter()


@router.post("/", response_model=Token)
async def auth(login: Login,
                users: UserRepository = Depends(get_user_repository)):
    user = await users.get_by_email(login.email)
    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect credentials.")
    return Token(
        access_token=create_access_token({"sub": user.email}),
        token_type="Bearer"
    )
