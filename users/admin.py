from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'tg_chat_id')
    search_fields = ('email',)
    ordering = ('email',)
