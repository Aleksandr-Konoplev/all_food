from django.contrib import admin
from table_reservation.models import Reservation, Table


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "start_at", "end_at")
    list_filter = (
        "table",
        "start_at",
    )
    search_fields = ("owner__email",)
    ordering = ("start_at",)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("id", "num_table", "num_of_seats")
    list_filter = ("num_of_seats",)
