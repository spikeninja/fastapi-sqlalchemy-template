import random
import smtplib
from datetime import datetime, UTC
from email.mime.text import MIMEText


def send_email(
    body: str,
    subject: str,
    recipients: list[str],
    smtp_server: str,
    smtp_port: int,
    smtp_email: str,
    smtp_password: str,
):
    """"""

    msg = MIMEText(body)
    msg["From"] = smtp_email
    msg["Subject"] = subject
    msg["To"] = ", ".join(recipients)
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, recipients, msg.as_string())


def generate_code(length: int) -> str:
    """"""
    alphabet, generated = "0123456789", ""

    for i in range(length):
        generated += random.choice(alphabet)

    return generated


def utcnow():
    """"""
    return datetime.now(UTC).replace(tzinfo=None)
