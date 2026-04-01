from datetime import datetime

from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.models import ContentForSite
from table_reservation.forms import ReservationForm
from table_reservation.models import Reservation, Table
from users.models import User


def create_base_content():
    for name_tag in ['greeting', 'main_img']:
        ContentForSite.objects.create(name_tag=name_tag, title=name_tag, text=name_tag)


def create_test_user(email, password='strong-pass-123', **extra_fields):
    user = User.objects.create(email=email, **extra_fields)
    user.set_password(password)
    user.save()
    return user


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


class ReservationViewsTests(TestCase):
    def setUp(self):
        create_base_content()
        self.user = create_test_user(
            email='guest@example.com',
            password='strong-pass-123',
            first_name='Guest',
        )
        self.other_user = create_test_user(
            email='other@example.com',
            password='strong-pass-123',
            first_name='Other',
        )
        self.moderator = create_test_user(
            email='moderator@example.com',
            password='strong-pass-123',
            first_name='Moderator',
        )
        moderator_group = Group.objects.create(name='moderator')
        self.moderator.groups.add(moderator_group)
        self.table = Table.objects.create(
            num_table=2,
            num_of_seats=4,
            description='Quiet corner',
            min_deposit=4500,
        )
        self.reservation = Reservation.objects.create(
            owner=self.user,
            table=self.table,
            start_at=self.aware_datetime(2026, 4, 10, 12, 0),
            end_at=self.aware_datetime(2026, 4, 10, 13, 0),
            deposit=self.table.min_deposit,
        )

    @staticmethod
    def aware_datetime(year, month, day, hour, minute):
        return timezone.make_aware(datetime(year, month, day, hour, minute))

    def test_create_view_redirects_anonymous_user(self):
        response = self.client.get(reverse('table_reservation:reservation-create'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)

    def test_create_view_shows_busy_lines_for_selected_day(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('table_reservation:reservation-create'), {'day': '2026-04-10'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Стол 2, занятое время: 12:00 - 13:00')

    def test_create_view_creates_reservation_with_owner_and_deposit(self):
        self.client.force_login(self.user)
        second_table = Table.objects.create(
            num_table=3,
            num_of_seats=2,
            description='Balcony',
            min_deposit=7000,
        )

        response = self.client.post(
            reverse('table_reservation:reservation-create'),
            data={
                'start_at': '2026-04-10 14:00',
                'end_at': '2026-04-10 15:00',
                'table': second_table.pk,
            },
        )

        self.assertRedirects(response, reverse('table_reservation:reservation-list'))
        reservation = Reservation.objects.get(owner=self.user, table=second_table)
        self.assertEqual(reservation.deposit, second_table.min_deposit)

    def test_list_view_shows_only_owner_reservations_for_regular_user(self):
        Reservation.objects.create(
            owner=self.other_user,
            table=self.table,
            start_at=self.aware_datetime(2026, 4, 10, 15, 0),
            end_at=self.aware_datetime(2026, 4, 10, 16, 0),
            deposit=self.table.min_deposit,
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse('table_reservation:reservation-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'guest@example.com')
        self.assertNotContains(response, 'other@example.com')

    def test_list_view_shows_all_reservations_for_moderator(self):
        Reservation.objects.create(
            owner=self.other_user,
            table=self.table,
            start_at=self.aware_datetime(2026, 4, 10, 15, 0),
            end_at=self.aware_datetime(2026, 4, 10, 16, 0),
            deposit=self.table.min_deposit,
        )
        self.client.force_login(self.moderator)

        response = self.client.get(reverse('table_reservation:reservation-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'guest@example.com')
        self.assertContains(response, 'other@example.com')

    def test_update_view_recalculates_deposit(self):
        self.client.force_login(self.user)
        second_table = Table.objects.create(
            num_table=4,
            num_of_seats=6,
            description='Family',
            min_deposit=9000,
        )

        response = self.client.post(
            reverse('table_reservation:reservation-update', kwargs={'pk': self.reservation.pk}),
            data={
                'start_at': '2026-04-10 13:30',
                'end_at': '2026-04-10 14:30',
                'table': second_table.pk,
            },
        )

        self.assertRedirects(response, reverse('table_reservation:reservation-list'))
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.table, second_table)
        self.assertEqual(self.reservation.deposit, second_table.min_deposit)

    def test_delete_view_removes_reservation(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('table_reservation:reservation-delete', kwargs={'pk': self.reservation.pk})
        )

        self.assertRedirects(response, reverse('table_reservation:reservation-list'))
        self.assertFalse(Reservation.objects.filter(pk=self.reservation.pk).exists())
