from accounts.factories import CustomUserFactory
from django.test import TestCase, tag
from django.urls import reverse_lazy

from .factories import ExpenseCategoryFactory, ExpenseFactory
from .models import Expense


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

    @tag("x")
    def test_user_create_expenses_success(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse_lazy("expenses:expenses-list-create"), data=self.cleaned_data
        )
        print(response.content)
        print(Expense.objects.all())
