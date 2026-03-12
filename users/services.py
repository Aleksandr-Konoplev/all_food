from django.shortcuts import get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.core.mail import get_connection, EmailMessage
from config.settings import EMAIL_SERVICES

from users.models import User


def custom_send_email(service, subject, body, recipient_list):
    config = EMAIL_SERVICES[service]

    connection = get_connection(
        backend='django.core.mail.backends.smtp.EmailBackend',
        host=config['HOST'],
        port=config['PORT'],
        username=config['USER'],
        password=config['PASSWORD'],
    )

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=config['USER'],
        to=recipient_list,
        connection=connection
    )

    email.send()


def email_verification(request: HttpRequest, token) -> HttpResponse:
    pass


def telegram_verification(request: HttpRequest, token) -> HttpResponse:
    pass


def phone_number_verification(request: HttpRequest, token) -> HttpResponse:
    pass


if __name__ == '__main__':
    test_text = 'Test text to func custom_send_email.'
    recipients = ['konoplev-ne@mail.ru', 'konoplev.a.a0000@gmail.com']
    custom_send_email(service='main', subject='test subj', body=test_text, recipient_list=recipients)