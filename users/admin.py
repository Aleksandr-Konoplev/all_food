from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ('email', 'is_staff', 'is_active', 'tg_chat_id')
    search_fields = ('email',)
    ordering = ('email',)

    # Определяет поля и оформление на форме создания нового пользователя
    add_fieldsets = (
        (
            None,  # группа без заголовка
            {
                'classes': ('wide',),  # CSS-класс для широкого отображения формы
                'fields': (
                    'email',  # поле email
                    'password1',  # пароль
                    'password2',  # подтверждение пароля
                    'is_staff',  # флаг персонала
                    'is_active',  # флаг активности пользователя
                    'tg_chat_id',
                ),
            },
        ),
    )

    # Определяет группы полей и их порядок на странице редактирования существующего пользователя
    fieldsets = (
        (None, {'fields': ('email', 'tg_chat_id', 'phone_number', 'password',)}),  # Контакты и пароль
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active',)}),  # Права и роли пользователя
        ('Important dates', {'fields': ('last_login',)}),  # Дата последнего входа
    )
