from django.urls import path
from table_reservation.views import (
    ReservationCreateView,
    ReservationListView,
    ReservationDetailView,
    ReservationUpdateView,
    ReservationDeleteView,
)

from table_reservation.apps import TableReservationConfig

app_name = TableReservationConfig.name

urlpatterns = [
    path("create/", ReservationCreateView.as_view(), name="reservation-create"),
    path("list/", ReservationListView.as_view(), name="reservation-list"),
    path("<int:pk>/detail/", ReservationDetailView.as_view(), name="reservation-detail"),
    path("<int:pk>/update/", ReservationUpdateView.as_view(), name="reservation-update"),
    path("<int:pk>/delete/", ReservationDeleteView.as_view(), name="reservation-delete"),
]
