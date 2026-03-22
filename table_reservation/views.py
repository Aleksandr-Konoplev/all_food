from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.dateparse import parse_date

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from table_reservation.models import Reservation, Table
from table_reservation.forms import ReservationForm
from table_reservation.mixins import OwnerOrModerReservationQuerysetMixin
from core.mixins import AddTextContentMixin


# CRUD Reservation
class ReservationCreateView(AddTextContentMixin, LoginRequiredMixin, CreateView):
    """Создание бронирования с показом занятости столов по выбранному дню."""

    model = Reservation
    form_class = ReservationForm
    template_name = 'table_reservation/reservation_form.html'  # noqa
    success_url = reverse_lazy('table_reservation:reservation-list')

    @staticmethod
    def _get_selected_day(day_value: str | None):
        """ Возвращает выбранную дату из query params или сегодняшнюю дату. """
        if day_value:
            selected_day = parse_date(day_value)
            if selected_day:
                return selected_day
        return timezone.localdate()

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст список занятости по всем столам на конкретный день.
        В выборку попадают только бронирования, у которых start_at в выбранных сутках.
        Формат каждой строки: "Стол N, занятое время: HH:MM - HH:MM, ..."
        """

        context = super().get_context_data(**kwargs)

        # День для фильтрации приходит через GET-параметр day (YYYY-MM-DD).
        selected_day = self._get_selected_day(self.request.GET.get('day'))

        tables = Table.objects.order_by('num_table')

        # Получаем брони, у которых дата начала (start_at) совпадает с выбранным днем.
        reservations = Reservation.objects.filter(
            start_at__date=selected_day,
        ).select_related('table').order_by('table__num_table', 'start_at')

        # Группируем брони по ID стола для быстрого доступа в цикле вывода.
        reservations_by_table = {}
        for reservation in reservations:
            reservations_by_table.setdefault(reservation.table_id, []).append(reservation)

        # Получаем список строк броней
        tables_busy_lines = []
        for table in tables:
            table_reservations = reservations_by_table.get(table.pk, [])
            # Резервы одного столика
            intervals = []
            for reservation in table_reservations:
                intervals.append(
                    f'{timezone.localtime(reservation.start_at).strftime("%H:%M")} - '
                    f'{timezone.localtime(reservation.end_at).strftime("%H:%M")}'
                )

            busy_time = ', '.join(intervals) if intervals else 'нет бронирований'
            tables_busy_lines.append(
                f'Стол {table.num_table}, занятое время: {busy_time}'
            )

        context['selected_day'] = selected_day.isoformat()
        context['tables_busy_lines'] = tables_busy_lines

        # Передаем в шаблон карту депозитов для мгновенного обновления отображаемой суммы.
        form = context.get('form')
        context['table_deposits'] = getattr(form, 'table_deposits', {}) if form else {}
        return context

    def form_valid(self, form):
        """ Добавляем владельца и сохраняем депозит строго из минимального депозита столика. """
        form.instance.owner = self.request.user
        form.instance.deposit = form.cleaned_data['table'].min_deposit
        return super().form_valid(form)


class ReservationListView(AddTextContentMixin, LoginRequiredMixin, OwnerOrModerReservationQuerysetMixin, ListView):
    model = Reservation
    template_name = 'table_reservation/reservations_list.html'  # type: ignore
    context_object_name = 'reservations'


class ReservationDetailView(AddTextContentMixin, LoginRequiredMixin, OwnerOrModerReservationQuerysetMixin, DetailView):
    model = Reservation
    template_name = 'table_reservation/reservation_detail.html'  # type: ignore
    context_object_name = 'reservation'


class ReservationUpdateView(AddTextContentMixin, LoginRequiredMixin, OwnerOrModerReservationQuerysetMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'table_reservation/reservation_form.html'  # type: ignore
    success_url = reverse_lazy('table_reservation:reservation-list')

    def get_context_data(self, **kwargs):
        """ Передаем карту депозитов и при редактировании брони. """
        context = super().get_context_data(**kwargs)
        form = context.get('form')
        context['table_deposits'] = getattr(form, 'table_deposits', {}) if form else {}
        return context

    def form_valid(self, form):
        """ При редактировании депозит также пересчитывается только по выбранному столику. """
        form.instance.deposit = form.cleaned_data['table'].min_deposit
        return super().form_valid(form)


class ReservationDeleteView(AddTextContentMixin, LoginRequiredMixin, OwnerOrModerReservationQuerysetMixin, DeleteView):
    model = Reservation
    template_name = 'table_reservation/confirm_delete.html'  # type: ignore
    success_url = reverse_lazy('table_reservation:reservation-list')
