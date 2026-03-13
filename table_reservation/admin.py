from django.contrib import admin
from table_reservation.models import Reservation, Table


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'date_visit', 'time_visit')
    list_filter = ('table', 'time_visit', 'date_visit')
    search_fields = ('client__email',)
    ordering = ('date_visit', 'time_visit',)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'num_table', 'num_of_seats')
    list_filter = ('num_of_seats',)