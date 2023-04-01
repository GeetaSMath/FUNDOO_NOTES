from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.reverse import reverse

from note.util import JWT


@shared_task(bind=True)
def send_mail_func(self,first_name,recipient):
    # print(first_name)
    # print(recipient)
    token = JWT().encode(data={"email": recipient})
    # token = JWT().encode(data=first_name)
    send_mail(
        subject='verify_token',
        message=f'{settings.BASE_URL}/verify_token/{token}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient],
       )
