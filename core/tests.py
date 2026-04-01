from io import StringIO
from unittest.mock import MagicMock, mock_open, patch

from django.contrib.auth.models import AnonymousUser, Group
from django.core.management import call_command
from django.test import RequestFactory, TestCase
from django.urls import reverse

from core.forms import FeedbackForm
from core.mixins import AddBaseContentMixin
from core.models import ContentForSite, Feedback
from core.services import custom_send_email
from users.models import User
from users.templatetags.users_groups import has_group


def create_base_content():
    content_items = [
        ('greeting', 'Welcome'),
        ('address', 'Test address'),
        ('phone', '+79990000000'),
        ('working_hours', '10:00-22:00'),
        ('restaurant_description', 'Restaurant description'),
        ('history_restaurant', 'History'),
        ('mission_and_values', 'Mission'),
        ('people_chef_cook', 'Chef'),
        ('people_hall_team', 'Hall team'),
        ('people_admin', 'Admin'),
        ('description_team', 'Team'),
        ('main_img', ''),
        ('promo_1', 'Promo 1'),
    ]
    for name_tag, text in content_items:
        ContentForSite.objects.create(name_tag=name_tag, text=text, title=name_tag.title())


def create_test_user(email, password='strong-pass-123', **extra_fields):
    user = User.objects.create(email=email, **extra_fields)
    user.set_password(password)
    user.save()
    return user


class FeedbackFormTests(TestCase):
    def test_form_prefills_authenticated_user_contacts(self):
        user = User.objects.create(
            email='client@example.com',
            first_name='Anna',
            phone_number='+79990000000',
        )
        user.set_password('strong-pass-123')
        user.save()

        form = FeedbackForm(user=user)

        self.assertEqual(form.fields['user_name'].initial, user.first_name)
        self.assertEqual(form.fields['phone'].initial, user.phone_number)
        self.assertEqual(form.fields['email'].initial, user.email)


class CoreViewsTests(TestCase):
    def setUp(self):
        create_base_content()
        self.factory = RequestFactory()
        self.user = create_test_user(
            email='user@example.com',
            password='strong-pass-123',
            first_name='User',
        )
        self.moderator = create_test_user(
            email='moderator@example.com',
            password='strong-pass-123',
            first_name='Moderator',
        )
        moderator_group = Group.objects.create(name='moderator')
        self.moderator.groups.add(moderator_group)

    def test_home_page_renders_and_contains_feedback_form(self):
        response = self.client.get(reverse('core:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Оставьте сообщение')
        self.assertContains(response, 'Restaurant description')

    def test_home_page_post_saves_feedback_for_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('core:home'),
            data={
                'user_name': 'Anna',
                'phone': '+79991112233',
                'email': 'anna@example.com',
                'body': 'Нужен столик у окна',
            },
        )

        self.assertRedirects(response, reverse('core:home'))
        feedback = Feedback.objects.get()
        self.assertEqual(feedback.owner, self.user)
        self.assertEqual(feedback.body, 'Нужен столик у окна')

    def test_about_page_renders(self):
        response = self.client.get(reverse('core:about'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'History')
        self.assertContains(response, 'Mission')

    def test_content_list_is_available_for_moderator(self):
        self.client.force_login(self.moderator)

        response = self.client.get(reverse('core:content-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'greeting')

    def test_content_list_is_forbidden_for_regular_user(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('core:content-list'))

        self.assertEqual(response.status_code, 403)

    def test_content_update_changes_text(self):
        self.client.force_login(self.moderator)
        content_item = ContentForSite.objects.get(name_tag='greeting')

        response = self.client.post(
            reverse('core:content-update', kwargs={'pk': content_item.pk}),
            data={
                'name_tag': content_item.name_tag,
                'text': 'Updated greeting',
                'title': content_item.title,
            },
        )

        self.assertEqual(response.status_code, 302)
        content_item.refresh_from_db()
        self.assertEqual(content_item.text, 'Updated greeting')

    def test_feedback_detail_and_delete_work_for_moderator(self):
        feedback = Feedback.objects.create(
            owner=self.user,
            user_name='Anna',
            phone='+79991112233',
            email='anna@example.com',
            body='Нужен звонок администратора',
        )
        self.client.force_login(self.moderator)

        detail_response = self.client.get(reverse('core:feedback-detail', kwargs={'pk': feedback.pk}))
        delete_response = self.client.post(reverse('core:feedback-delete', kwargs={'pk': feedback.pk}))

        self.assertEqual(detail_response.status_code, 200)
        self.assertRedirects(delete_response, reverse('core:feedbacks-list'))
        self.assertFalse(Feedback.objects.filter(pk=feedback.pk).exists())


class CoreHelpersTests(TestCase):
    def test_add_base_content_mixin_adds_common_blocks(self):
        create_base_content()

        class DummyParent:
            def get_context_data(self, **kwargs):
                return {'existing': 'value', **kwargs}

        class DummyView(AddBaseContentMixin, DummyParent):
            pass

        context = DummyView().get_context_data(extra='field')

        self.assertEqual(context['existing'], 'value')
        self.assertEqual(context['extra'], 'field')
        self.assertEqual(context['greeting'].name_tag, 'greeting')
        self.assertEqual(context['promo_items'].count(), 1)

    @patch('core.services.EmailMessage')
    @patch('core.services.get_connection')
    def test_custom_send_email_uses_selected_service(self, mock_get_connection, mock_email_message):
        connection = object()
        message = MagicMock()
        mock_get_connection.return_value = connection
        mock_email_message.return_value = message

        custom_send_email('main', 'Subject', 'Body', ['client@example.com'])

        mock_get_connection.assert_called_once()
        mock_email_message.assert_called_once()
        self.assertEqual(mock_email_message.call_args.kwargs['connection'], connection)
        message.send.assert_called_once()

    def test_has_group_filter_checks_group_membership(self):
        user = create_test_user(email='member@example.com', password='strong-pass-123')
        moderator_group = Group.objects.create(name='moderator')
        user.groups.add(moderator_group)

        self.assertTrue(has_group(user, 'moderator'))
        self.assertFalse(has_group(user, 'manager'))
        self.assertFalse(has_group(AnonymousUser(), 'moderator'))


class ManagementCommandsTests(TestCase):
    @patch('core.management.commands.load_default_data.call_command')
    @patch('core.management.commands.load_default_data.Command._truncate_tables')
    def test_load_default_data_adds_tables_when_no_reservations(self, mock_truncate, mock_call_command):
        out = StringIO()

        call_command('load_default_data', '--yes', stdout=out)

        truncate_tables = mock_truncate.call_args.args[0]
        loaded_fixtures = [call.args[1] for call in mock_call_command.call_args_list]
        self.assertIn('table_reservation_table', truncate_tables)
        self.assertIn('core/fixtures/default_table.json', loaded_fixtures)

    @patch('core.management.commands.load_default_data.call_command')
    @patch('core.management.commands.load_default_data.Command._truncate_tables')
    def test_load_default_data_skips_tables_when_reservations_exist(self, mock_truncate, mock_call_command):
        user = create_test_user(email='client@example.com', password='strong-pass-123')
        table = self._create_table()
        self._create_reservation(user, table)
        out = StringIO()

        call_command('load_default_data', '--yes', stdout=out)

        truncate_tables = mock_truncate.call_args.args[0]
        loaded_fixtures = [call.args[1] for call in mock_call_command.call_args_list]
        self.assertNotIn('table_reservation_table', truncate_tables)
        self.assertNotIn('core/fixtures/default_table.json', loaded_fixtures)

    @patch('builtins.open', new_callable=mock_open)
    @patch('core.management.commands.dumpfixture.call_command')
    @patch('builtins.input', return_value='YES')
    def test_dumpfixture_writes_dumpdata_to_output(self, mock_input, mock_call_command, mock_file):
        call_command('dumpfixture', 'auth.Group', 'fixture.json')

        mock_file.assert_called_once_with('fixture.json', 'w', encoding='utf-8')
        mock_call_command.assert_called_once()

    @patch('builtins.input', side_effect=['admin@example.com'])
    @patch('core.management.commands.custom_csu.getpass', side_effect=['bad-pass', 'bad-pass-2', 'good-pass', 'good-pass'])
    def test_custom_csu_retries_until_passwords_match(self, mock_getpass, mock_input):
        out = StringIO()

        call_command('custom_csu', stdout=out)

        user = User.objects.get(email='admin@example.com')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password('good-pass'))

    @patch('core.management.commands.full_reset_db.connection')
    @patch('builtins.input', return_value='YES')
    def test_full_reset_db_executes_truncate_for_existing_tables(self, mock_input, mock_connection):
        cursor = MagicMock()
        mock_connection.introspection.table_names.return_value = ['users_user', 'core_contentforsite']
        mock_connection.cursor.return_value.__enter__.return_value = cursor
        out = StringIO()

        call_command('full_reset_db', stdout=out)

        executed_sql = cursor.execute.call_args.args[0]
        self.assertIn('TRUNCATE TABLE', executed_sql)
        self.assertIn('users_user', executed_sql)

    def _create_table(self):
        from django.utils import timezone

        from table_reservation.models import Table

        return Table.objects.create(
            num_table=1,
            num_of_seats=4,
            description='Window table',
            min_deposit=3000,
        )

    def _create_reservation(self, user, table):
        from datetime import datetime

        from django.utils import timezone

        from table_reservation.models import Reservation

        Reservation.objects.create(
            owner=user,
            table=table,
            start_at=timezone.make_aware(datetime(2026, 4, 10, 12, 0)),
            end_at=timezone.make_aware(datetime(2026, 4, 10, 13, 0)),
            deposit=table.min_deposit,
        )
