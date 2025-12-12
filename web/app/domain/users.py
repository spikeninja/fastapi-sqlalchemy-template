from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass(slots=True)
class User:
    id: UUID
    name: str
    email: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
