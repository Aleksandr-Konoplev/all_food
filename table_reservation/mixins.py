from django.http import HttpRequest

from table_reservation.models import Reservation


class OwnerOrModerReservationQuerysetMixin:
    """
    Разрешает доступ к объекту его владельцу, а также суперпользователю и модератору.
    """
    request: HttpRequest

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='moderator').exists():
            return Reservation.objects.all()
        return Reservation.objects.filter(owner=user)