from http import HTTPStatus

from accounts.tests import CustomUserFactory
from budgets_manager.tests.factories.budget_manager_factory import BudgetManagerFactory
from django.contrib.messages import constants, get_messages
from django.test import TestCase
from django.urls import reverse_lazy
from expenses.tests.factories import ExpenseCategoryFactory
from expenses.types import Type
from incomes.tests.factories import IncomeFactory
from subscription.tests.factories import PlanFactory, SubscriptionFactory


class LimitManagerCreateTestCase(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.budget_manager = BudgetManagerFactory.create(user=self.user)
        self.plan = PlanFactory.create()
        self.income = IncomeFactory.create(
            user=self.user, budget=self.budget_manager, amount=1000
        )
        self.subscription_factory = SubscriptionFactory.create(
            user=self.user, plan=self.plan
        )
        self.expenses_category = ExpenseCategoryFactory.create(user=self.user)
        # self.expenses = ExpenseFactory.create(user=self.user, budget=self.budget_manager)

        self.limit_create = reverse_lazy("manager:limits-list-create")

    def test_user_create_limit_manager_success(self):
        self.client.force_login(self.user)

        data = {
            "type": Type.NEEDS,
            "category_expense": self.expenses_category.id,
            "amount": 100,
        }

        response = self.client.post(self.limit_create, data=data)

        message = list(get_messages(response.wsgi_request))[0]

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(message.level, constants.SUCCESS)

    def test_user_create_limit_manager_failure(self):
        self.client.force_login(self.user)

        data = {}
        response = self.client.post(
            self.limit_create, data=data, content_type="application/json"
        )

        message = list(get_messages(response.wsgi_request))[0]

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(message.level, constants.ERROR)
