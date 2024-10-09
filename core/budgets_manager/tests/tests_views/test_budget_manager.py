from http import HTTPStatus

from accounts.tests import CustomUserFactory
from budgets_manager.models import BudgetManager
from budgets_manager.tests.factories.budget_manager_factory import BudgetManagerFactory
from django.contrib.messages import constants, get_messages
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse_lazy
from subscription.models import Subscription
from subscription.tests.factories import PlanFactory, SubscriptionFactory


class TestBudgetManagerCreateView(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.plan = PlanFactory.create()
        self.subscription_factory = SubscriptionFactory.create(
            user=self.user, plan=self.plan
        )
        self.create_budget_reverse_url = reverse_lazy("manager:budget-list-create")

    def get_payment_url(self, payment_id: int) -> str:
        return reverse_lazy("payment", kwargs={"payment_id": payment_id})

    def test_create_budget_manager_success(self):
        self.client.force_login(self.user)

        data = {
            "title": "Family",
            "color": "#FF0000",
            "savings_percentage": 20,
            "wants_percentage": 40,
            "needs_percentage": 40,
        }

        response = self.client.post(self.create_budget_reverse_url, data=data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(BudgetManager.objects.filter(user=self.user).exists())
        self.assertRedirects(
            response, self.get_payment_url(Subscription.objects.last().payment.pk)
        )

    def test_create_budget_manager_with_empty_data_failure(self):
        self.client.force_login(self.user)

        data = {}

        response = self.client.post(self.create_budget_reverse_url, data=data)

        message = list(get_messages(response.wsgi_request))[0]

        self.assertEqual(message.level, constants.ERROR)


class TestBudgetManagerInfoView(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.budget_manager = BudgetManagerFactory.create(user=self.user)
        self.plan = PlanFactory.create()
        self.subscription_factory = SubscriptionFactory.create(
            user=self.user, plan=self.plan
        )
        self.budget_pk = BudgetManager.objects.get(user=self.user).pk

    @staticmethod
    def get_budget_reverse_url(pk: int) -> str:
        return reverse_lazy("manager:budget-detail-info", kwargs={"pk": pk})

    def test_get_budget_manager_success(self):
        self.client.force_login(self.user)

        response = self.client.get(self.get_budget_reverse_url(pk=self.budget_pk))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.budget_manager.title)

    def test_unauthenticated_user_get_budget_manager_failure(self):
        response = self.client.get(self.get_budget_reverse_url(pk=self.budget_pk))
        expected_url = f"{reverse_lazy('accounts:login')}?next={self.get_budget_reverse_url(pk=self.budget_pk)}"

        self.assertRedirects(response, expected_url)


class TestBudgetManagerUpdateView(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.budget_manager = BudgetManagerFactory.create(user=self.user)
        self.plan = PlanFactory.create()
        self.subscription_factory = SubscriptionFactory.create(
            user=self.user, plan=self.plan
        )
        self.budget_pk = BudgetManager.objects.get(user=self.user).pk
        self.clean_data = {
            "title": "Family",
            "color": "#FF0000",
            "savings_percentage": 40,
            "wants_percentage": 20,
            "needs_percentage": 40,
        }

    @staticmethod
    def get_budget_update_url(pk: int) -> str:
        return reverse_lazy("manager:budget-detail-update", kwargs={"pk": pk})

    def test_user_update_budget_manager_success(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.get_budget_update_url(pk=self.budget_pk), data=self.clean_data
        )

        message = list(get_messages(response.wsgi_request))[0]

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(message.level, constants.SUCCESS)

        self.assertRedirects(response, reverse_lazy("home"))

    def test_user_update_budget_manager_with_fail_data_failure(self):
        self.client.force_login(self.user)

        fail_data = self.clean_data.copy()
        fail_data["savings_percentage"] = 20

        with self.assertRaises(ValidationError):
            self.client.post(self.get_budget_update_url(pk=self.budget_pk), fail_data)
