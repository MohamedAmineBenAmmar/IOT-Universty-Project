import sys
sys.path.insert(0, '.')

import asyncio
from time import sleep

from modules.email.controllers.email_controller import email_sender
from settings.settings import NOTIFICATION_EMAIL_TEMPLATE


async def send_notification():
    success = False
    while not success:
        success = True
        try:
            await email_sender.send_email_async(sys.argv[1].capitalize(), sys.argv[2],
            {'title': f'{sys.argv[1].capitalize()} Alert', 'msg': f'Alert we detected a raise in the {sys.argv[1]} !!!'}, NOTIFICATION_EMAIL_TEMPLATE)
        except Exception as exception:
            print(type(exception).__name__)
            print(exception.__class__.__name__)
            print(exception.__class__.__qualname__)
            if type(exception).__name__ == 'SMTPDataError':
                success = False
                sleep(2)



asyncio.run(send_notification())