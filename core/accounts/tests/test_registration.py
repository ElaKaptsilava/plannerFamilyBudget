from accounts.models import CustomUser
from accounts.tests import CustomUserFactory
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status


class TestRegisterUser(TestCase):
    def setUp(self):
        self.user_build = CustomUserFactory.build()
        self.cleaned_data: dict = {
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
        CustomUser.objects.get(email=self.user_build.email)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse_lazy("manager:budget-list-create"))
        self.assertTrue(
            get_user_model().objects.filter(email=self.user_build.email).exists()
        )

    def test_register_view_post_invalid_form(self):
        data = dict()

        response = self.client.post(reverse_lazy("accounts:register"), data)
        registration_form = response.context["registration_form"].fields

        email_errors = registration_form["email"].error_messages["required"]
        username_errors = registration_form["username"].error_messages["required"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(email_errors, "This field is required.")
        self.assertEqual(username_errors, "This field is required.")

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
        registration_form = response.context["registration_form"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            get_user_model().objects.filter(email=self.cleaned_data["email"]).exists()
        )
        self.assertFormError(
            registration_form,
            "email",
            f"Email {self.user_build.email} is already in use.",
        )

    def test_register_view_post_password_mismatch(self):
        self.cleaned_data["password2"] = self.cleaned_data["password2"][:3]

        response = self.client.post(
            reverse_lazy("accounts:register"), self.cleaned_data
        )
        registration_form = response.context["registration_form"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFormError(
            registration_form, "password2", "The two password fields didn’t match."
        )
