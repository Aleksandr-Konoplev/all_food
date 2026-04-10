from unittest.mock import patch
import os
from dotenv import load_dotenv

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import Group
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core.models import ContentForSite
from users.forms import ResendConfirmationForm, StyledPasswordResetForm, StyledSetPasswordForm, UserRegisterForm, UserUpdateForm
from users.models import User


load_dotenv()

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

    def test_resend_confirmation_form_contains_email(self):
        form = ResendConfirmationForm()

        self.assertIn('email', form.fields)
        self.assertEqual(form.fields['email'].label, 'Email')

    def test_password_reset_forms_have_custom_labels(self):
        reset_form = StyledPasswordResetForm()
        user = create_test_user(email='set-password@example.com', password='strong-pass-123', first_name='Set')
        set_password_form = StyledSetPasswordForm(user=user)

        self.assertEqual(reset_form.fields['email'].label, 'Email')
        self.assertEqual(set_password_form.fields['new_password1'].label, 'Новый пароль')


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

    @patch('users.services.custom_send_email')
    def test_register_view_creates_inactive_user_and_sends_email(self, mock_send_email):
        response = self.client.post(
            reverse('users:register'),
            data={
                'email': 'new@example.com',
                'password1': os.getenv('TEST_PASSWORD'),
                'password2': os.getenv('TEST_PASSWORD'),
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

    @patch('users.services.custom_send_email')
    def test_resend_confirmation_renews_token_for_inactive_user(self, mock_send_email):
        inactive_user = create_test_user(
            email='inactive@example.com',
            password='strong-pass-123',
            first_name='Inactive',
            is_active=False,
            token='old-token',
        )

        response = self.client.post(
            reverse('users:resend-confirmation'),
            data={'email': inactive_user.email},
        )

        inactive_user.refresh_from_db()
        self.assertRedirects(response, reverse('users:login'))
        self.assertNotEqual(inactive_user.token, 'old-token')
        mock_send_email.assert_called_once()

    @patch('users.services.custom_send_email')
    def test_resend_confirmation_does_not_send_for_active_user(self, mock_send_email):
        old_token = self.user.token

        response = self.client.post(
            reverse('users:resend-confirmation'),
            data={'email': self.user.email},
        )

        self.user.refresh_from_db()
        self.assertRedirects(response, reverse('users:login'))
        self.assertEqual(self.user.token, old_token)
        mock_send_email.assert_not_called()

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

    def test_password_reset_sends_email_for_existing_user(self):
        response = self.client.post(
            reverse('users:password-reset'),
            data={'email': self.user.email},
        )

        self.assertRedirects(response, reverse('users:password-reset-done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Сброс пароля All Food', mail.outbox[0].subject)
        self.assertIn('/users/reset/', mail.outbox[0].body)

    def test_password_reset_for_unknown_email_still_redirects(self):
        response = self.client.post(
            reverse('users:password-reset'),
            data={'email': 'missing@example.com'},
        )

        self.assertRedirects(response, reverse('users:password-reset-done'))
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_confirm_updates_password(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        confirm_url = reverse('users:password-reset-confirm', kwargs={'uidb64': uid, 'token': token})

        response = self.client.get(confirm_url)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            response.url,
            data={
                'new_password1': 'New-strong-pass-123',
                'new_password2': 'New-strong-pass-123',
            },
        )

        self.assertRedirects(response, reverse('users:password-reset-complete'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('New-strong-pass-123'))
