from datetime import datetime

from sqlalchemy import String, Index, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.resources import Base


class UsersModel(Base):
    __tablename__ = "users"

    __table_args__ = (
        # for soft-delete mechanism
        Index(
            "idx_users__email__deleted_at",
            "email",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    deleted_at: Mapped[datetime | None] = mapped_column(default=None)

    email: Mapped[str] = mapped_column(String(128), unique=True)
    name: Mapped[str] = mapped_column(String(64))
    hashed_password: Mapped[str] = mapped_column(String(256))
