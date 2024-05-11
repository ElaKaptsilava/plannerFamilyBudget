from django.contrib.auth import get_user_model
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

    def test_login(self):
        data = {"email": self.user_build.email, "password": self.user_build.password}

        response = self.client.post(reverse_lazy("accounts:login"), data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse_lazy("home"))

    @tag("x")
    def test_login_with_invalid_email(self):
        data = {"email": self.user_build.username, "password": self.user_build.password}

        response = self.client.post(reverse_lazy("accounts:login"), data)
        login_form = response.context["login_form"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFormError(login_form, "email", "Enter a valid email address.")


class TestRegisterUser(TestCase):
    def setUp(self):
        self.user_build = CustomUserFactory.build(is_active=False)
        self.cleaned_data = {
            "email": self.user_build.email,
            "username": self.user_build.username,
            "last_name": self.user_build.last_name,
            "first_name": self.user_build.first_name,
            "password1": self.user_build.password,
            "password2": self.user_build.password,
        }

    def test_register_view_post_success(self):
        response = self.client.post(
            reverse_lazy("accounts:register"), self.cleaned_data
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse_lazy("accounts:login"))
        self.assertTrue(
            get_user_model().objects.filter(email=self.user_build.email).exists()
        )

    def test_register_view_post_invalid_form(self):
        data = {}

        response = self.client.post(reverse_lazy("accounts:register"), data)
        form = response.context["form"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFormError(form, "email", "This field is required.")
        self.assertFormError(form, "username", "This field is required.")

    def test_register_view_post_existing_email(self):
        get_user_model().objects.create_user(
            email=self.cleaned_data["email"],
            username=self.cleaned_data["username"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            password=self.cleaned_data["password1"],
        )

        response = self.client.post(
            reverse_lazy("accounts:register"), self.cleaned_data
        )
        form = response.context["form"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            get_user_model().objects.filter(email=self.cleaned_data["email"]).exists()
        )
        self.assertFormError(form, "email", "This email is already in use.")

    def test_register_view_post_password_mismatch(self):
        self.cleaned_data["password2"] = self.cleaned_data["password2"][:3]

        response = self.client.post(
            reverse_lazy("accounts:register"), self.cleaned_data
        )
        form = response.context["form"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFormError(form, "password2", "The two password fields didn’t match.")
