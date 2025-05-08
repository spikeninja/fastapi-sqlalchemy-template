import os
from dataclasses import dataclass

from sqlalchemy import URL


@dataclass
class Config:
    algorithm: str
    secret_key: str
    access_token_expire_minutes: int

    pg_host: str
    pg_port: int
    pg_user: str
    pg_pass: str
    database: str

    logger_level: str
    logger_filename: str

    # BACKGROUND TASKS
    cache_url: str
    broker_url: str
    backend_url: str

    rate_limiter_url: str

    # WEBSOCKET SERVER
    ws_pubsub_url: str
    ws_pubsub_name: str
    ws_server_port: int

    # SMTP
    smtp_port: int
    smtp_user: str
    smtp_email: str
    smtp_server: str
    smtp_password: str

    # S3
    s3_bucket_name: str
    s3_private_key: str
    s3_public_key: str

    @property
    def postgresql_url(self) -> str:
        return URL.create(
            drivername="postgresql+psycopg",
            host=self.pg_host,
            port=self.pg_port,
            password=self.pg_pass,
            username=self.pg_user,
            database=self.database,
        ).render_as_string(hide_password=False)

    @property
    def async_postgresql_url(self) -> str:
        return URL.create(
            drivername="postgresql+psycopg",
            host=self.pg_host,
            port=self.pg_port,
            password=self.pg_pass,
            username=self.pg_user,
            database=self.database,
        ).render_as_string(hide_password=False)

    @classmethod
    def from_env(cls):
        """"""

        return cls(
            algorithm="HS256",
            secret_key=os.environ["SECRET_KEY"],
            pg_host=os.environ["POSTGRES_HOST"],
            pg_port=int(os.environ["POSTGRES_PORT"]),
            pg_user=os.environ["POSTGRES_USER"],
            pg_pass=os.environ["POSTGRES_PASSWORD"],
            database=os.environ["POSTGRES_DB"],
            logger_level=os.environ["LOGGER_LEVEL"],
            logger_filename=os.environ["LOGGER_FILENAME"],
            cache_url=os.environ["CACHE_URL"],
            broker_url=os.environ["BROKER_URL"],
            backend_url=os.environ["BACKEND_URL"],
            rate_limiter_url=os.environ["RATE_LIMITER_URL"],
            ws_pubsub_url=os.environ["WS_PUBSUB_URL"],
            ws_pubsub_name=os.environ["WS_PUBSUB_NAME"],
            ws_server_port=int(os.environ["WS_SERVER_PORT"]),
            smtp_port=int(os.environ["SMTP_PORT"]),
            smtp_user=os.environ["SMTP_USER"],
            smtp_email=os.environ["SMTP_EMAIL"],
            smtp_server=os.environ["SMTP_SERVER"],
            smtp_password=os.environ["SMTP_PASSWORD"],
            s3_bucket_name="some_bucket",
            s3_public_key="lskdjfklsdjfklsdfjl",
            s3_private_key=":lsdjf;aksjfaskfjsjflsdajfa;sdkfjsldf",
            access_token_expire_minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]),
        )


def load_config():
    """"""
    return Config.from_env()
