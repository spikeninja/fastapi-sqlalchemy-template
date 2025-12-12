from dishka import make_async_container
from dishka.integrations.taskiq import setup_dishka
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from app.ioc import AppProvider
from app.core.config import load_config

broker = ListQueueBroker(
    url=load_config().broker_url,
).with_result_backend(
    RedisAsyncResultBackend(
        redis_url=load_config().backend_url,
    )
)

setup_dishka(
    broker=broker,
    container=make_async_container(AppProvider()),
)
