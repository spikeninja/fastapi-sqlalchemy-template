from app.tasks.broker import broker
from app.repositories import Repositories
from app.utils.functions import send_email
from dishka.integrations.taskiq import FromDishka, inject


@broker.task
def task_send_email(recipients: list[str], subject: str, body: str):
    """"""

    send_email(recipients=recipients, subject=subject, body=body)


@broker.task
@inject
async def task_doing_smth(
    something: str,
    repositories: FromDishka[Repositories],
):
    """"""

    # doing smth
