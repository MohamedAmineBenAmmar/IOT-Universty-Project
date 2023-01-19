from fastapi import APIRouter, BackgroundTasks
from modules.email.controllers.email_controller import email_sender
from settings.settings import NOTIFICATION_EMAIL_TEMPLATE

router = APIRouter(
    prefix='/test',
    tags=['Tests']
)

@router.get('/send-email/asynchronous')
async def send_email_asynchronous():
    await email_sender.send_email_async('Temperature Alert','achrafb.s2015@gmail.com',
        {'title': 'Temperature ', 'name': 'Alert we detected a raise in the temperature !!!'}, NOTIFICATION_EMAIL_TEMPLATE)
    return 'Success'

