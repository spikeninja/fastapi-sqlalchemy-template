from pydantic import BaseModel, Field
from app.schemas.users import UserPublic


class AuthResponse(BaseModel):
    token: str
    user: UserPublic


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str = Field(min_length=8)
    password_repeat: str = Field(min_length=8)
