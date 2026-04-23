from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser

class UserRegistrationTests(TestCase):
    def test_registration_view_status_code(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_profile_creation_signal(self):
        """Assure creating a CustomUser automatically spawns a Profile instance organically."""
        user = CustomUser.objects.create_user(username='sig_test', password='123')
        self.assertIsNotNone(user.profile)
