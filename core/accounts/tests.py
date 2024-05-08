from django.test import TestCase

from .factories import CustomUserFactory
from .models import CustomUser


class TestAccounts(TestCase):
    def setUp(self):
        self.user = CustomUserFactory()

    def test_create_user(self):
        get_all_users = CustomUser.objects.all()
        self.assertEqual(len(get_all_users), 1)
        self.assertEqual(get_all_users[0].email, self.user.email)
