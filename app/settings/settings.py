from pydantic import BaseSettings
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()


EMAIL_TEMPLATES_PATH = './templates/email'
NOTIFICATION_EMAIL_TEMPLATE = 'notification_email.html'


class Settings(BaseSettings):
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str


settings = Settings()