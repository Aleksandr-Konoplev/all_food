from django.shortcuts import get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse

from users.models import User


def email_verification(request: HttpRequest, token) -> HttpResponse:
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None
    user.save()
    return redirect(reverse("users:login"))
