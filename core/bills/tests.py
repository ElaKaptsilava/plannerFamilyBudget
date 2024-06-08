from accounts.factories import CustomUserFactory
from django.test import TestCase


class BillsTests(TestCase):
    def setUp(self):
        self.user = CustomUserFactory()
