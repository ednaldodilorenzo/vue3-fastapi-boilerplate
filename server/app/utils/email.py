from app.config import email_settings
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


conf = ConnectionConfig(
    MAIL_USERNAME=email_settings.username,
    MAIL_PASSWORD=email_settings.password,
    MAIL_FROM=email_settings.username,
    MAIL_PORT=email_settings.port,
    MAIL_SERVER=email_settings.server,
    USE_CREDENTIALS=email_settings.use_credentials,
    VALIDATE_CERTS=email_settings.validate_certs,
    MAIL_STARTTLS=email_settings.mail_starttls,
    MAIL_SSL_TLS=email_settings.mail_ssl_tls,
)


async def send_email_async(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="email.html")


async def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html",
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message, template_name="email.html")
