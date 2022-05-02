import os

# Security stuff
ACCESS_TOKEN_EXPIRE_MINUTES = 5
SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

# Database stuff
PG_HOST = "postgres_db"
PG_USER = os.getenv(
    "POSTGRES_USER",
    default="PROJECT_NAME_user"
)
PG_PASS = os.getenv(
    "POSTGRES_PASSWORD",
    default="example"
)
DATABASE = os.getenv(
    "POSTGRES_DB",
    default="PROJECT_NAME_db"
)
