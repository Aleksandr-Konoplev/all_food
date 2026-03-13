from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django import forms

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from table_reservation.models import Reservation
from table_reservation.forms import ReservationForm
from table_reservation.mixins import OwnerReservationQuerysetMixin


# CRUD Reservation
class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'table_reservation/reservation_form.html'  # type: ignore
    success_url = reverse_lazy('table_reservation:reservation-list')

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)


class ReservationListView(LoginRequiredMixin, OwnerReservationQuerysetMixin, ListView):
    model = Reservation
    template_name = 'table_reservation/reservations_list.html'  # type: ignore
    context_object_name = 'reservations'


class ReservationDetailView(LoginRequiredMixin, OwnerReservationQuerysetMixin, DetailView):
    model = Reservation
    template_name = 'table_reservation/reservation_detail.html'  # type: ignore
    context_object_name = 'reservation'


class ReservationUpdateView(LoginRequiredMixin, OwnerReservationQuerysetMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'table_reservation/reservation_form.html'  # type: ignore
    success_url = reverse_lazy('table_reservation:reservation-list')


class ReservationDeleteView(LoginRequiredMixin, OwnerReservationQuerysetMixin, DeleteView):
    model = Reservation
    template_name = 'table_reservation/confirm_delete.html'  # type: ignore
    success_url = reverse_lazy('table_reservation:reservation-list')
