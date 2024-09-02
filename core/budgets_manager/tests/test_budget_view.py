from http import HTTPStatus

from accounts.tests import CustomUserFactory
from budgets_manager.models import BudgetManager
from budgets_manager.tests.factories import BudgetManagerFactory
from django.test import TestCase
from django.urls import reverse_lazy


class UpdateBudgetViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget = BudgetManagerFactory.create(user=self.user)

    def detail_url(self, pk):
        return reverse_lazy("manager:budget-detail-update", kwargs={"pk": pk})

    def test_update_budget_success(self):
        self.client.force_login(self.user)
        data = {
            "savings_percentage": 10,
            "wants_percentage": 50,
            "needs_percentage": 40,
        }
        response = self.client.post(
            self.detail_url(self.budget.pk),
            data,
        )

        get_budget = BudgetManager.objects.get(user=self.user)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(get_budget.wants_percentage, data["wants_percentage"])
        self.assertEqual(get_budget.savings_percentage, data["savings_percentage"])
        self.assertEqual(get_budget.needs_percentage, data["needs_percentage"])

    def test_update_budget_fail(self):
        self.client.force_login(self.user)
        data = {
            "savings_percentage": 10,
            "wants_percentage": 40,
            "needs_percentage": 40,
        }
        response = self.client.post(
            reverse_lazy("manager:budget-detail-update", kwargs={"pk": self.budget.pk}),
            data,
        )
        messages = list(response.context["messages"])

        self.assertEqual(messages[0].message, "Check budget data!")

    # def test_user_create_budget_success(self):
    #     BudgetManager.objects.all().delete()
    #     self.client.force_login(self.user)
    #
    #     budgets_data = {
    #         "savings_percentage": 20,
    #         "needs_percentage": 40,
    #         "wants_percentage": 40,
    #     }
    #
    #     create_budget_response = self.client.post(
    #         reverse_lazy("manager:budget-list-create"), budgets_data
    #     )
    #     expected_home_url = reverse_lazy("home")
    #
    #     self.assertEqual(create_budget_response.url, expected_home_url)
    #     self.assertEqual(create_budget_response.status_code, HTTPStatus.FOUND)
