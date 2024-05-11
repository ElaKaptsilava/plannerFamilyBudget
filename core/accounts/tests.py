from django.test import TestCase

from .factories import CustomUserFactory
from .models import CustomUser


class TestLoginUser(TestCase):
    def setUp(self):
        self.user_build = CustomUserFactory.build(is_active=False)
        self.user = CustomUser.objects.create_user(
            email=self.user_build.email,
            username=self.user_build.username,
            last_name=self.user_build.last_name,
            first_name=self.user_build.first_name,
            password=self.user_build.password,
            is_active=False,
        )
