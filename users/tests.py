from unittest.mock import patch

from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from core.models import ContentForSite
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


def create_base_content():
    for name_tag in ['greeting', 'main_img']:
        ContentForSite.objects.create(name_tag=name_tag, title=name_tag, text=name_tag)


def create_test_user(email, password='strong-pass-123', **extra_fields):
    user = User.objects.create(email=email, **extra_fields)
    user.set_password(password)
    user.save()
    return user


class EmailVerificationTests(TestCase):
    def test_email_verification_activates_user_and_clears_token(self):
        user = User.objects.create(
            email='new-user@example.com',
            first_name='New',
            is_active=False,
            token='verify-token',
        )
        user.set_password('strong-pass-123')
        user.save()

        response = self.client.get(reverse('users:email-confirm', kwargs={'token': user.token}))

        user.refresh_from_db()
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(user.is_active)
        self.assertIsNone(user.token)


class UsersFormsTests(TestCase):
    def test_register_form_contains_expected_fields(self):
        form = UserRegisterForm()

        self.assertIn('email', form.fields)
        self.assertIn('password1', form.fields)
        self.assertEqual(form.fields['password1'].label, 'Пароль')

    def test_update_form_contains_profile_fields(self):
        form = UserUpdateForm()

        self.assertIn('first_name', form.fields)
        self.assertIn('phone_number', form.fields)
        self.assertEqual(form.fields['email'].help_text, 'Введите вашу электронную почту')


class UsersViewsTests(TestCase):
    def setUp(self):
        create_base_content()
        self.user = create_test_user(
            email='user@example.com',
            password='strong-pass-123',
            first_name='User',
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

    @patch('users.views.custom_send_email')
    def test_register_view_creates_inactive_user_and_sends_email(self, mock_send_email):
        response = self.client.post(
            reverse('users:register'),
            data={
                'email': 'new@example.com',
                'password1': 'Very-strong-pass-123',
                'password2': 'Very-strong-pass-123',
                'phone_number': '+79991112233',
                'first_name': 'New',
                'last_name': 'User',
            },
        )

        self.assertRedirects(response, reverse('users:login'))
        user = User.objects.get(email='new@example.com')
        self.assertFalse(user.is_active)
        self.assertIsNotNone(user.token)
        mock_send_email.assert_called_once()

    def test_moderator_can_open_users_list(self):
        self.client.force_login(self.moderator)

        response = self.client.get(reverse('users:users-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user@example.com')

    def test_regular_user_cannot_open_users_list(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('users:users-list'))

        self.assertEqual(response.status_code, 403)

    def test_regular_user_can_open_only_own_profile(self):
        self.client.force_login(self.user)

        own_response = self.client.get(reverse('users:user-detail', kwargs={'pk': self.user.pk}))
        other_response = self.client.get(reverse('users:user-detail', kwargs={'pk': self.other_user.pk}))

        self.assertEqual(own_response.status_code, 200)
        self.assertEqual(other_response.status_code, 404)

    def test_user_update_changes_profile_data(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('users:user-update', kwargs={'pk': self.user.pk}),
            data={
                'email': 'user@example.com',
                'phone_number': '+79990000001',
                'first_name': 'Updated',
                'last_name': 'Name',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.phone_number, '+79990000001')

    def test_user_delete_removes_profile(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('users:user-delete', kwargs={'pk': self.user.pk}))

        self.assertRedirects(response, reverse('users:login'))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
