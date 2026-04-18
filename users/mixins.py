from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

from users.models import User


class UserAccessQuerysetMixin(LoginRequiredMixin):
    """
    Ограничивает queryset пользователей по роли текущего пользователя.

    - superuser и moderator получают доступ ко всем пользователям;
    - обычный пользователь получает доступ только к своей записи.
    """

    request: HttpRequest

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.groups.filter(name='moderator').exists():
            return User.objects.all()

        return User.objects.filter(pk=user.pk)


class ModeratorRequiredMixin(LoginRequiredMixin):
    """
    Разрешает доступ только superuser и пользователю из группы 'moderator'.
    Используется для представлений, где нужен полный доступ ко всем объектам (ListView)
    """

    request: HttpRequest

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user

        if not (user.is_superuser or user.groups.filter(name='moderator').exists()):
            raise PermissionDenied("У вас нет доступа к этому разделу.")

        return super().dispatch(request, *args, **kwargs)
