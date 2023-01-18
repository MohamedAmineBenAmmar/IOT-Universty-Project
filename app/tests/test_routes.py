from fastapi import APIRouter, BackgroundTasks
from modules.email.controllers.email_controller import email_sender

router = APIRouter(
    prefix='/test',
    tags=['Tests']
)

@router.get('/send-email/asynchronous')
async def send_email_asynchronous():
    await email_sender.send_email_async('Hello World','mohamedamine.benammar@etudiant-isi.utm.tn',
    {'title': 'Hello World', 'name': 'John Doe'})
    return 'Success'

