from django.test import TestCase

from core.forms import FeedbackForm
from users.models import User


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
