from django.test import TestCase, tag
from django.urls import reverse_lazy
from rest_framework import status

from ..models import CustomUser
from .factories import CustomUserFactory


class TestLoginLogoutUser(TestCase):
    def setUp(self):
        self.user_build = CustomUserFactory.build()
        self.user = CustomUser.objects.create_user(
            email=self.user_build.email,
            username=self.user_build.username,
            last_name=self.user_build.last_name,
            first_name=self.user_build.first_name,
            password=self.user_build.password,
            is_active=False,
        )

    def test_login_success(self):
        data = {
            "email": self.user_build.email,
            "password": self.user_build.password,
        }

        response = self.client.post(reverse_lazy("accounts:login"), data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse_lazy("home"))

    def test_login_with_invalid_email(self):
        data: dict = {"email": "", "password": self.user_build.password}

        response = self.client.post(reverse_lazy("accounts:login"), data)
        login_form = response.context["login_form"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFormError(login_form, "email", "This field is required.")

    @tag("test")
    def test_login_case_insensitive_user_success(self):
        data: dict = {
            "email": self.user_build.email.upper(),
            "password": self.user_build.password,
        }

        response = self.client.post(reverse_lazy("accounts:login"), data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse_lazy("home"))