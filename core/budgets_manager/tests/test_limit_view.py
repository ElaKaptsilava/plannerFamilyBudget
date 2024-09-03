from http import HTTPStatus

from accounts.tests import CustomUserFactory
from budgets_manager.models import LimitManager
from budgets_manager.tests.factories import BudgetManagerFactory, LimitManagerFactory
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from django.urls import reverse_lazy
from expenses import types
from expenses.tests.factories import ExpenseCategoryFactory
from incomes.tests.factories import IncomeFactory
from runningCosts.tests.factories import RunningCostCategoryFactory
from targets.tests import TargetFactory


class LimitViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budgetmanager = BudgetManagerFactory.create(user=self.user)
        self.income = IncomeFactory.create(user=self.user)
        self.category_expense = ExpenseCategoryFactory.create(user=self.user)
        self.category_running_cost = RunningCostCategoryFactory.create(user=self.user)
        self.target = TargetFactory.create(user=self.user)
        self.limit = LimitManagerFactory.build()

        self.limit_create = reverse_lazy("manager:limits-list-create")
        self.limit_delete = reverse_lazy("manager:limits-delete-multiple")
        self.limit_update = reverse_lazy(
            "manager:limits-detail-update", kwargs={"pk": self.target.pk}
        )

        self.danger_level = 40
        self.success_level = 25

        self.clean_data_cost = {
            "type": types.Type.NEEDS,
            "category_running_cost": self.category_running_cost.pk,
            "amount": 1,
        }
        self.clean_data_target = {
            "type": types.Type.WANTS,
            "target": self.target.pk,
            "amount": self.income.amount,
        }
        self.clean_data_expense = {
            "type": self.category_expense.type,
            "category_expense": self.category_expense.pk,
            "amount": 1,
        }

    def test_create_limit_success(self):
        self.client.force_login(self.user)

        response = self.client.post(self.limit_create, self.clean_data_cost)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(
            LimitManager.objects.get(
                budget_manager=self.budgetmanager,
                category_running_cost=self.category_running_cost,
            )
        )

        response = self.client.post(self.limit_create, self.clean_data_expense)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(
            LimitManager.objects.get(
                budget_manager=self.budgetmanager,
                category_expense=self.category_expense,
            )
        )

    def test_create_limit_fail(self):
        self.client.force_login(self.user)

        with self.assertRaises(ValidationError):
            self.client.post(self.limit_create, self.clean_data_target)

    def test_create_limit_with_invalid_data(self):
        self.client.force_login(self.user)

        data = {}

        response = self.client.post(self.limit_create, data)

        messages = list(get_messages(response.wsgi_request))[0]

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(messages.level, self.danger_level)

    def test_delete_selected_limits_success(self):
        self.client.force_login(self.user)

        limit = LimitManagerFactory.create(
            budget_manager=self.budgetmanager,
            type=types.Type.WANTS,
            target=self.target,
            amount=1,
        )
        limit1 = LimitManagerFactory.create(
            budget_manager=self.budgetmanager,
            type=types.Type.NEEDS,
            category_running_cost=self.category_running_cost,
            amount=1,
        )

        self.assertEqual(LimitManager.objects.count(), 2)

        selected = [limit.pk, limit1.pk]

        response = self.client.post(self.limit_delete, {"selected": selected})
        messages = list(get_messages(response.wsgi_request))[0]

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(LimitManager.objects.count())
        self.assertEqual(messages.level, self.success_level)

    def test_delete_not_selected_limits(self):
        self.client.force_login(self.user)

        response = self.client.post(self.limit_delete, {"selected": []})

        messages = list(get_messages(response.wsgi_request))[0]

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(messages.level, self.danger_level)

    @tag("test")
    def test_update_limit_success(self):
        self.client.force_login(self.user)

        self.clean_data_target.update({"amount": 1})
        response = self.client.post(self.limit_create, self.clean_data_target)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(LimitManager.objects.all())

        amount = 2
        self.clean_data_target.update({"amount": amount})

        response = self.client.post(self.limit_update, self.clean_data_target)
        messages = list(get_messages(response.wsgi_request))[0]
        print(messages)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(messages.level, self.success_level)

        self.assertEqual(
            LimitManager.objects.get(
                budget_manager=self.budgetmanager, target=self.target
            ).amount,
            amount,
        )
