import random
import smtplib
from email.mime.text import MIMEText

from app.core.config import settings


def send_email(recipients: list[str], subject: str, body: str):
    msg = MIMEText(body)
    msg["From"] = settings.smtp_email
    msg["Subject"] = subject
    msg["To"] = ", ".join(recipients)
    with smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port) as server:
        server.login(settings.smtp_email, settings.smtp_password)
        server.sendmail(settings.smtp_email, recipients, msg.as_string())


def generate_code(length: int) -> str:
    """"""
    alphabet, generated = "0123456789", ""

    for i in range(length):
        generated += random.choice(alphabet)

    return generated
