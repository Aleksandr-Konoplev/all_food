from django.test import TestCase
from django.urls import reverse

from users.models import User


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
