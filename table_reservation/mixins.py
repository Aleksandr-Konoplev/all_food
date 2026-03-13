from table_reservation.models import Reservation


class OwnerReservationQuerysetMixin:
    def get_queryset(self):
        return Reservation.objects.filter(owner=self.request.user)