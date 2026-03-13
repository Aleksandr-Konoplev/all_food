from django.contrib import admin
from table_reservation.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'date_visit', 'time_visit')
    list_filter = ('table', 'time_visit', 'date_visit')
    search_fields = ('client',)