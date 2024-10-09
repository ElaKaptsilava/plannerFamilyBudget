from http import HTTPStatus

from accounts.tests import CustomUserFactory
from budgets_manager.tests.factories.budget_manager_factory import BudgetManagerFactory
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.http import urlencode
from expenses.models import Expense
from expenses.tests.factories import ExpenseCategoryFactory, ExpenseFactory
from incomes.tests.factories import IncomeFactory
from rest_framework import status


class ExpenseListTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()

        self.budget = BudgetManagerFactory.create(user=self.user)
        self.income = IncomeFactory.create(user=self.user, budget=self.budget)

        self.category_create1 = ExpenseCategoryFactory.create(user=self.user)
        self.category_create2 = ExpenseCategoryFactory.create(user=self.user)

        self.expenses_build1 = ExpenseFactory.create(
            user=self.user, category=self.category_create1, budget=self.budget
        )
        self.expenses_build2 = ExpenseFactory.create(
            user=self.user, category=self.category_create2, budget=self.budget
        )

        self.expenses_list_url = reverse_lazy("expenses:expenses-list")

    def test_user_get_expenses_success(self):
        self.client.force_login(self.user)

        response = self.client.get(self.expenses_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context["expenses"]), 2)

    def test_unauthorized_user_get_expenses_fail(self):
        response = self.client.get(self.expenses_list_url)

        query_string = urlencode({"next": self.expenses_list_url})

        expected_redirect_url = f"{reverse_lazy('accounts:login')}?{query_string}"

        self.assertRedirects(response, expected_redirect_url)


class ExpensesCreateTests(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget = BudgetManagerFactory.create(user=self.user)
        self.income = IncomeFactory.create(user=self.user, budget=self.budget)
        self.category_create = ExpenseCategoryFactory.create(user=self.user)
        self.expenses_build = ExpenseFactory.build()
        self.cleaned_data = {
            "category": self.category_create.pk,
            "amount": self.expenses_build.amount,
            "datetime": self.expenses_build.datetime,
        }
        self.expenses_create_url = reverse_lazy("expenses:expenses-list-create")

    def test_user_create_expense_success(self):
        self.client.force_login(self.user)

        response = self.client.post(self.expenses_create_url, data=self.cleaned_data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Expense.objects.count(), 1)

    def test_unauthorized_user_create_expense_fail(self):
        response = self.client.post(self.expenses_create_url, data=self.cleaned_data)

        query_string = urlencode({"next": self.expenses_create_url})

        expected_redirect_url = f"{reverse_lazy('accounts:login')}?{query_string}"

        self.assertFalse(Expense.objects.all())
        self.assertRedirects(response, expected_redirect_url)

    def test_user_create_expense_with_invalid_data(self):
        self.client.force_login(self.user)

        invalid_data = {}

        response = self.client.post(self.expenses_create_url, data=invalid_data)

        form_errors = response.context["form"].errors

        self.assertTrue(form_errors)

        self.assertIn("category", form_errors)
        self.assertIn("amount", form_errors)
        self.assertIn("datetime", form_errors)

        self.assertEqual(form_errors["category"][0], "This field is required.")
        self.assertEqual(form_errors["amount"][0], "This field is required.")
        self.assertEqual(form_errors["datetime"][0], "This field is required.")


class ExpensesUpdateTests(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget = BudgetManagerFactory.create(user=self.user)

        self.category_create = ExpenseCategoryFactory.create(user=self.user)
        self.expenses = ExpenseFactory.create(
            user=self.user, category=self.category_create, budget=self.budget
        )
        self.success_level = 25
        self.error_level = 40

    @staticmethod
    def get_url_detail(pk: int) -> reverse_lazy:
        return reverse_lazy("expenses:expenses-detail-update", kwargs={"pk": pk})

    def test_update_expense_success(self):
        self.client.force_login(self.user)

        detail_update = self.get_url_detail(self.expenses.pk)
        valid_data = {
            "category": self.category_create.pk,
            "amount": 100,
            "datetime": self.expenses.datetime,
        }

        response = self.client.post(detail_update, data=valid_data)

        message = list(get_messages(response.wsgi_request))[0]

        self.assertEqual(message.level, self.success_level)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_expense_fail(self):
        self.client.force_login(self.user)

        detail_update = self.get_url_detail(self.expenses.pk)
        invalid_data = {}

        response = self.client.post(detail_update, data=invalid_data)

        message = list(get_messages(response.wsgi_request))[0]

        self.assertEqual(message.level, self.error_level)


class ExpensesDeleteTests(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget = BudgetManagerFactory.create(user=self.user)

        self.category_create = ExpenseCategoryFactory.create(user=self.user)
        self.expenses = ExpenseFactory.create(
            user=self.user, category=self.category_create, budget=self.budget
        )
        self.expenses = ExpenseFactory.create(
            user=self.user, category=self.category_create, budget=self.budget
        )
        self.expenses = ExpenseFactory.create(
            user=self.user, category=self.category_create, budget=self.budget
        )
        self.success_level = 25
        self.info_level = 20
        self.url_delete_multiple = reverse_lazy(
            "expenses:expenses-list-delete-multiple"
        )

    def test_delete_expense_success(self):
        self.client.force_login(self.user)

        selected_expenses = [self.category_create.pk]
        response = self.client.post(
            self.url_delete_multiple, data={"selected_expenses": selected_expenses}
        )

        message = list(get_messages(response.wsgi_request))[0]

        self.assertEqual(message.level, self.success_level)
        self.assertEqual(Expense.objects.count(), 3)

    def test_delete_expense_with_empty_data(self):
        self.client.force_login(self.user)
        selected = []

        response = self.client.post(
            self.url_delete_multiple, data={"selected_expenses": selected}
        )

        message = list(get_messages(response.wsgi_request))[0]

        self.assertEqual(message.level, self.info_level)
        self.assertEqual(Expense.objects.count(), 3)
