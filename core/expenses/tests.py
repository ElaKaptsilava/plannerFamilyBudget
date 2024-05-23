from accounts.factories import CustomUserFactory
from django.test import TestCase, tag
from django.urls import reverse_lazy
from django.utils.http import urlencode
from rest_framework import status

from .factories import ExpenseCategoryFactory, ExpenseFactory
from .models import Expense


class ExpenseListTestCase(TestCase):
    def setUp(self):
        self.user1 = CustomUserFactory.create()

        self.category_create1 = ExpenseCategoryFactory.create()
        self.category_create2 = ExpenseCategoryFactory.create()

        self.expenses_build1 = ExpenseFactory.build()
        self.expenses_build2 = ExpenseFactory.build()

        self.expenses_create_url = reverse_lazy("expenses:expenses-list-create")
        self.expenses_list_url = reverse_lazy("expenses:expenses-list")

    def test_user_get_expenses_success(self):
        self.client.force_login(self.user1)

        cleaned_data1 = {
            "category": self.category_create1.pk,
            "amount": self.expenses_build1.amount,
            "datetime": self.expenses_build1.datetime,
        }
        cleaned_data2 = {
            "category": self.category_create2.pk,
            "amount": self.expenses_build2.amount,
            "datetime": self.expenses_build2.datetime,
        }

        self.client.post(self.expenses_create_url, cleaned_data1)
        self.client.post(self.expenses_create_url, cleaned_data2)

        response = self.client.get(self.expenses_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context["expenses"]), 2)

    @tag("x")
    def test_unauthorized_user_get_expenses_fail(self):
        response = self.client.get(self.expenses_list_url)

        query_string = urlencode({"next": self.expenses_list_url})

        expected_redirect_url = f"{reverse_lazy('accounts:login')}?{query_string}"

        self.assertRedirects(response, expected_redirect_url)


class ExpensesCreateTests(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.category_create = ExpenseCategoryFactory.create()
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
