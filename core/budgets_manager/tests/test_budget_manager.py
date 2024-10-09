import unittest

from accounts.tests import CustomUserFactory
from budgets_manager.tests.factories.budget_manager_factory import BudgetManagerFactory
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from expenses.tests.factories import ExpenseCategoryFactory, ExpenseFactory
from incomes.tests.factories import IncomeFactory


class TestBudgetManager(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget_manager = BudgetManagerFactory.create(user=self.user)
        self.income_amount = 1000
        self.expense_amount = 100
        self.income = IncomeFactory.create(
            user=self.user, budget=self.budget_manager, amount=self.income_amount
        )
        self.expense_category = ExpenseCategoryFactory.create(user=self.user)
        self.expense = ExpenseFactory.create(
            user=self.user,
            budget=self.budget_manager,
            amount=self.expense_amount,
            category=self.expense_category,
        )

    def test_str_representation(self):
        self.assertEqual(
            str(self.budget_manager), f"{self.user.first_name.upper()}'s Budget Plan"
        )

    def test_repr_representation(self):
        needs_p = self.budget_manager.needs_percentage
        wants_p = self.budget_manager.wants_percentage
        savings_p = self.budget_manager.savings_percentage
        expected_repr = (
            f"Budget(user={self.budget_manager.user.username!r}, savings_percentage={savings_p}, "
            f"wants_percentage={wants_p}, needs_percentage={needs_p})"
        )
        self.assertEqual(repr(self.budget_manager), expected_repr)

    @tag("test")
    def test_clean_method_invalid(self):
        self.budget_manager.savings_percentage = 40.0
        self.budget_manager.wants_percentage = 30.0
        self.budget_manager.needs_percentage = 20.0
        with self.assertRaises(ValidationError):
            self.budget_manager.check_total_allocation()

    def test_get_annual_incomes(self):
        incomes = self.budget_manager.get_annual_incomes()
        self.assertEqual(incomes.count(), 1)
        self.assertEqual(incomes.first().amount, self.income_amount)

    def test_get_annual_expenses(self):
        expenses = self.budget_manager.get_annual_expenses()
        self.assertEqual(expenses.count(), 1)
        self.assertEqual(expenses.first().amount, self.expense_amount)

    def test_total_monthly_incomes_no_data(self):
        self.budget_manager.incomes.all().delete()
        self.assertEqual(self.budget_manager.total_monthly_incomes, 0.0)

    def test_total_monthly_expenses_no_data(self):
        self.budget_manager.expenses.all().delete()
        self.assertEqual(self.budget_manager.total_monthly_expenses, 0.0)

    def test_monthly_incomes_was_created(self):
        self.assertTrue(self.budget_manager.monthlyincomes_set)


if __name__ == "__main__":
    unittest.main()
