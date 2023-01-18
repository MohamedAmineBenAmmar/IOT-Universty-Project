from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from settings.settings import settings, EMAIL_TEMPLATES_PATH

class Email():
    def __init__(self) -> None:
        self.config = ConnectionConfig(
            MAIL_USERNAME=settings.mail_username,
            MAIL_PASSWORD=settings.mail_password,
            MAIL_FROM=settings.mail_from,
            MAIL_PORT=settings.mail_port,
            MAIL_SERVER=settings.mail_server,
            MAIL_FROM_NAME=settings.mail_from_name,       
            VALIDATE_CERTS=True,
            TEMPLATE_FOLDER=EMAIL_TEMPLATES_PATH,
            MAIL_SSL_TLS=False,
            MAIL_STARTTLS=True,
            USE_CREDENTIALS=True
        )

    async def send_email_async(self, subject: str, email_to: str, body: dict, template_name: str):
        message = MessageSchema(
            subject=subject,
            recipients=[email_to],
            template_body=body,
            subtype='html',
        )
        
        fm = FastMail(self.config)        
        await fm.send_message(message, template_name=template_name)



email_sender = Email()