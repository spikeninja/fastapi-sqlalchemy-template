import os

from sqlalchemy import URL
from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    secret_key: str = os.getenv('SECRET_KEY')

    pg_host: str = os.getenv("POSTGRES_HOST")
    pg_port: int = os.getenv("POSTGRES_PORT")
    pg_user: str = os.getenv("POSTGRES_USER")
    pg_pass: str = os.getenv("POSTGRES_PASSWORD")
    database: str = os.getenv("POSTGRES_DB")

    logger_level: str = os.getenv("LOGGER_LEVEL")
    logger_filename: str = os.getenv("LOGGER_FILENAME")

    # BACKGROUND TASKS
    cache_url: str = os.getenv("CACHE_URL")
    broker_url: str = os.getenv("BROKER_URL")
    backend_url: str = os.getenv("BACKEND_URL")

    rate_limiter_url: str = os.getenv("RATE_LIMITER_URL")

    # WEBSOCKET SERVER
    ws_pubsub_url: str = os.getenv("WS_PUBSUB_URL")
    ws_pubsub_name: str = os.getenv("WS_PUBSUB_NAME")
    ws_server_port: int = os.getenv("WS_SERVER_PORT")

    # SMTP
    smtp_port: int = os.getenv("SMTP_PORT")
    smtp_user: str = os.getenv('SMTP_USER')
    smtp_email: str = os.getenv('SMTP_EMAIL')
    smtp_server: str = os.getenv("SMTP_SERVER")
    smtp_password: str = os.getenv('SMTP_PASSWORD')

    @computed_field
    @property
    def postgresql_url(self) -> str:
        return URL.create(
            drivername="postgresql",
            host=self.pg_host,
            port=self.pg_port,
            password=self.pg_pass,
            username=self.pg_user,
            database=self.database
        ).render_as_string(hide_password=False)

    @computed_field
    @property
    def async_postgresql_url(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.pg_host,
            port=self.pg_port,
            password=self.pg_pass,
            username=self.pg_user,
            database=self.database,
        ).render_as_string(hide_password=False)


settings = Settings()
