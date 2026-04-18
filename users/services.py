import secrets

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse

from core.services import custom_send_email
from users.models import User


def send_activation_email(user: User, request: HttpRequest, regenerate_token: bool = False) -> bool:
    if user.is_active:
        return False

    if regenerate_token or not user.token:
        user.token = secrets.token_hex(16)
        user.save(update_fields=['token'])

    url = request.build_absolute_uri(reverse('users:email-confirm', kwargs={'token': user.token}))
    custom_send_email(
        'auto',
        'Активация аккаунта',
        f'Перейдите по ссылке: {url} для активации аккаунта.',
        [user.email],
    )
    return True


def resend_activation_email(email: str, request: HttpRequest) -> bool:
    user = User.objects.filter(email=email, is_active=False).first()

    if not user:
        return False

    return send_activation_email(user, request, regenerate_token=True)


def email_verification(request: HttpRequest, token) -> HttpResponse:
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None
    user.save()
    return redirect(reverse("users:login"))
