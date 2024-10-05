from datetime import datetime
from pydantic import BaseModel


class UserPublic(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None


class UserUpdateRequest(BaseModel):
    name: str


class UserDTO(BaseModel):
    id: int
    name: str
    email: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
