# Кастомный шаблонный тэг для проверки принадлежности пользователя к группе
from django import template

register = template.Library()

@register.filter
def has_group(user, group_name):
    return user.is_authenticated and user.groups.filter(name=group_name).exists()
