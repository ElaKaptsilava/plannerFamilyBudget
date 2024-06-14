from django.test import TestCase, tag
from django.urls import reverse_lazy
from http import HTTPStatus

from accounts.factories import CustomUserFactory
from accounts.models import CustomUser
from .factories import BudgetManagerFactory


class BudgetManagerTestCase(TestCase):
    def setUp(self):
        self.user_build = CustomUserFactory.build()
        self.budget_build = BudgetManagerFactory.build()

    @tag("test")
    def test_create_budget_when_user_registered(self):
        user_data = {
            "first_name": self.user_build.first_name,
            "last_name": self.user_build.last_name,
            "email": self.user_build.email,
            "password1": self.user_build.password,
            "password2": self.user_build.password,
            "username": self.user_build.username,
        }

        register_response = self.client.post(
            reverse_lazy("accounts:register"), user_data
        )

        user = CustomUser.objects.get(email=self.user_build.email)
        expected_budget_url = reverse_lazy(
            "manager:budget-list-create", kwargs={"user_id": user.pk}
        )

        self.assertEqual(register_response.url, expected_budget_url)

        budgets_data = {
            "savings_percentage": 20,
            "needs_percentage": 40,
            "wants_percentage": 40,
        }

        create_budget_response = self.client.post(expected_budget_url, budgets_data)
        expected_home_url = reverse_lazy("home", kwargs={"user_id": user.pk})

        self.assertEqual(create_budget_response.url, expected_home_url)
        self.assertEqual(create_budget_response.status_code, HTTPStatus.FOUND)