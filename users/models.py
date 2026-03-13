from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя
    """

    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=32, verbose_name='Имя')
    last_name = models.CharField(max_length=32, verbose_name='Фамилия', blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=20, verbose_name='Номер телефона', blank=True, null=True)
    tg_chat_id = models.CharField(unique=True, max_length=64, verbose_name='ID чата телеграм', blank=True, null=True)
    avatar = models.ImageField(
        upload_to='users/avatars/',
        default='users/avatars/default_ava.png',
        verbose_name='Аватар',
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} - {self.email} - {self.phone_number}'
