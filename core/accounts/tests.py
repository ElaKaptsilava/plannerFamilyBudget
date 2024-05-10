from django.test import TestCase, tag
from django.urls import reverse_lazy
from rest_framework import status

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

    @tag("x")
    def test_login_post_valid_credentials(self):
        response = self.client.post(
            reverse_lazy("accounts:login"),
            {"email": self.user.email, "password": self.user_build.password},
        )

        user_from_db = CustomUser.objects.get(email=self.user.email)

        self.assertTrue(user_from_db.is_active)
        self.assertRedirects(response, reverse_lazy("home"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_user_login_unsuccessful(self):
        response = self.client.post(
            reverse_lazy("accounts:login"),
            {"email": self.user.email, "password": self.user.password},
        )

        self.assertFalse(self.user.is_active)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_user_login(self):
        response = self.client.post(
            reverse_lazy("accounts:login"),
            {"email": "test123@gmail.com", "password": self.user.password},
        )
        self.assertRedirects(response, reverse_lazy("accounts:register"))


class TestRegisterUser(TestCase):
    pass
