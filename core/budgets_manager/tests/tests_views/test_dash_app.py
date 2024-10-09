import json
from http import HTTPStatus

from accounts.tests import CustomUserFactory
from budgets_manager.tests.factories.budget_manager_factory import BudgetManagerFactory
from django.test import TestCase
from django.urls import reverse_lazy
from incomes.tests.factories import IncomeFactory
from subscription.tests.factories import PlanFactory, SubscriptionFactory


class TestDashAppView(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget_manager = BudgetManagerFactory.create(user=self.user)
        self.plan = PlanFactory.create()
        self.subscription_factory = SubscriptionFactory.create(
            user=self.user, plan=self.plan
        )
        self.get_earnings_data_url = reverse_lazy("earnings-data")

    def test_user_get_earnings_data_success(self):
        self.client.force_login(self.user)

        response = self.client.get(self.get_earnings_data_url)
        expected_contains_response = [0.0] * 12

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, expected_contains_response)


class TestRevenueSourcesView(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget_manager = BudgetManagerFactory.create(user=self.user)
        self.plan = PlanFactory.create()
        self.subscription_factory = SubscriptionFactory.create(
            user=self.user, plan=self.plan
        )
        self.get_revenue_sources_url = reverse_lazy("revenue-sources")
        self.incomes_1 = IncomeFactory.create(
            user=self.user, budget=self.budget_manager
        )
        self.incomes_2 = IncomeFactory.create(
            user=self.user, budget=self.budget_manager
        )

    def test_user_get_revenue_sources_success(self):
        self.client.force_login(self.user)

        response = self.client.get(self.get_revenue_sources_url)
        data = json.loads(response.content)
        contains_amounts = data.get("amounts")

        expected_amounts_contains_response = [
            self.incomes_1.amount,
            self.incomes_2.amount,
        ]

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(contains_amounts, expected_amounts_contains_response)
