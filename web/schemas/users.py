from datetime import datetime
from pydantic import BaseModel


class UserCreate(BaseModel):
    id: str
    email: str
    username: str
    password: str
    created_date: datetime


class UserGet(BaseModel):
    id: str
    email: str
    username: str
    created_date: datetime
