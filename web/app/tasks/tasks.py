import asyncio

from app.core.config import Config
from app.tasks.broker import broker
from app.utils.functions import send_email
from app.gateways.users import UsersGateway
from dishka.integrations.taskiq import FromDishka, inject


@broker.task
def task_send_email(
    body: str,
    subject: str,
    recipients: list[str],
    config: FromDishka[Config],
):
    """"""

    send_email(
        body=body,
        subject=subject,
        recipients=recipients,
        smtp_port=config.smtp_port,
        smtp_email=config.smtp_email,
        smtp_server=config.smtp_server,
        smtp_password=config.smtp_password,
    )


@broker.task
@inject
async def task_doing_smth(
    param: str,
    users_gateway: FromDishka[UsersGateway],
):
    """"""
    print(f"Doing smth with {param}...")
    await asyncio.sleep(5)
    print("Done!")
