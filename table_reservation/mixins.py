from table_reservation.models import Reservation


class OwnerOrModerReservationQuerysetMixin:
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='moderator').exists():
            return Reservation.objects.all()
        return Reservation.objects.filter(owner=user)