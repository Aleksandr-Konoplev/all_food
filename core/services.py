from config.settings import EMAIL_SERVICES
from django.core.mail import get_connection, EmailMessage


def custom_send_email(service: str, subject: str, body: str, recipient_list: list[str]) -> None:
    """
    Кастомная функция отправки email, с возможностью выбора почтового сервиса
    :param service: определяет конфигурацию почтового сервиса из config/settings.py
    :param subject: тема письма
    :param body: тело письма
    :param recipient_list: список получателей
    :return:
    """
    config = EMAIL_SERVICES[service]

    connection = get_connection(
        backend='django.core.mail.backends.smtp.EmailBackend',
        host=config['HOST'],
        port=config['PORT'],
        username=config['USER'],
        password=config['PASSWORD'],
        use_tls=config['USE_TLS'],
        use_ssl=config['USE_SSL'],
    )

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=config['USER'],
        to=recipient_list,
        connection=connection
    )

    email.send()