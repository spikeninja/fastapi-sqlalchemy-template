import datetime

from pydantic import BaseModel, EmailStr, validator, constr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str
    # Validator here for password equivalence
