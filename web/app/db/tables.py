from sqlalchemy import String, Index, text, Table, Column, UUID, DateTime

from app.domain.users import User
from app.utils.functions import utcnow
from app.db.base import MAPPER_REGISTRY


users_table = Table(
    "users",
    MAPPER_REGISTRY.metadata,
    Column("id", UUID, primary_key=True),
    Column("created_at", DateTime, default=utcnow),
    Column("updated_at", DateTime, default=utcnow),
    Column("deleted_at", DateTime, default=None),
    Column("email", String(128), unique=True),
    Column("name", String(64)),
    Column("hashed_password", String(256)),
    Index(
        "idx_users__email__deleted_at",
        "email",
        unique=True,
        postgresql_where=text("deleted_at IS NULL"),
    ),
)

MAPPER_REGISTRY.map_imperatively(User, users_table)
