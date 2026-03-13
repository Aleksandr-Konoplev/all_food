from django.urls import reverse_lazy
from django import forms

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from table_reservation.models import Reservation
from table_reservation.forms import ReservationForm


# CRUD Reservation
class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'table_reservation/reservation_form.html'
    success_url = reverse_lazy('table_reservation:reservation-list')

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)


class ReservationListView(ListView):
    model = Reservation
    template_name = 'table_reservation/reservations_list.html'
    context_object_name = 'reservations'


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'table_reservation/reservation_detail.html'
    context_object_name = 'reservation'


class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'table_reservation/reservation_form.html'
    success_url = reverse_lazy('table_reservation:reservation-list')


class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'table_reservation/confirm_delete.html'
    success_url = reverse_lazy('table_reservation:reservation-list')
