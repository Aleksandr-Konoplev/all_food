from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from table_reservation.forms import ReservationForm
from table_reservation.models import Reservation, Table
from users.models import User


class ReservationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='guest@example.com',
            first_name='Guest',
        )
        self.user.set_password('strong-pass-123')
        self.user.save()
        self.table = Table.objects.create(
            num_table=1,
            num_of_seats=4,
            description='Near the window',
            min_deposit=3000,
        )

    @staticmethod
    def aware_datetime(year, month, day, hour, minute):
        return timezone.make_aware(datetime(year, month, day, hour, minute))

    def test_clean_sets_deposit_from_table(self):
        reservation = Reservation(
            owner=self.user,
            table=self.table,
            start_at=self.aware_datetime(2026, 4, 10, 12, 0),
            end_at=self.aware_datetime(2026, 4, 10, 13, 0),
            deposit=1,
        )

        reservation.full_clean()

        self.assertEqual(reservation.deposit, self.table.min_deposit)

    def test_clean_rejects_overlapping_reservations_for_same_table(self):
        Reservation.objects.create(
            owner=self.user,
            table=self.table,
            start_at=self.aware_datetime(2026, 4, 10, 12, 0),
            end_at=self.aware_datetime(2026, 4, 10, 13, 0),
            deposit=self.table.min_deposit,
        )
        conflicting_reservation = Reservation(
            owner=self.user,
            table=self.table,
            start_at=self.aware_datetime(2026, 4, 10, 12, 30),
            end_at=self.aware_datetime(2026, 4, 10, 13, 30),
            deposit=self.table.min_deposit,
        )

        with self.assertRaises(ValidationError) as exc:
            conflicting_reservation.full_clean()

        self.assertEqual(
            exc.exception.message_dict['table'],
            ['Этот столик уже забронирован на выбранное время.'],
        )


class ReservationFormTests(TestCase):
    def setUp(self):
        self.table = Table.objects.create(
            num_table=2,
            num_of_seats=2,
            description='Quiet corner',
            min_deposit=4500,
        )

    def test_form_adds_table_deposit_to_cleaned_data(self):
        form = ReservationForm(
            data={
                'start_at': '2026-04-10 12:00',
                'end_at': '2026-04-10 13:00',
                'table': self.table.pk,
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['deposit'], self.table.min_deposit)

    def test_form_rejects_start_time_not_divisible_by_fifteen_minutes(self):
        form = ReservationForm(
            data={
                'start_at': '2026-04-10 12:10',
                'end_at': '2026-04-10 13:00',
                'table': self.table.pk,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['start_at'], ['Время начала должно быть кратно 15 минутам.'])

    def test_form_rejects_end_time_before_start_time(self):
        form = ReservationForm(
            data={
                'start_at': '2026-04-10 13:00',
                'end_at': '2026-04-10 12:45',
                'table': self.table.pk,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors(), ['Время окончания должно быть позже времени начала.'])
