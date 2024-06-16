from accounts.factories import CustomUserFactory
from budgets_manager.tests.factories import BudgetManagerFactory
from django.test import TestCase, tag
from django.utils import timezone
from expenses.factories import ExpenseCategoryFactory
from incomes.factories import IncomeFactory


class BudgetManagerTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory()
        self.manager_budget = BudgetManagerFactory(user=self.user)
        self.expenses_category = ExpenseCategoryFactory(user=self.user)
        self.incomes = IncomeFactory(user=self.user, date=timezone.now())

    def test_calculate_monthly_income_when_user_add_more_incomes(self):
        self.assertEqual(
            self.manager_budget.calculate_monthly_income, self.incomes.amount
        )

        income_1 = IncomeFactory(user=self.user, date=timezone.now())
        expected_total_incomes = self.incomes.amount + income_1.amount

        self.assertEqual(
            self.manager_budget.calculate_monthly_income, expected_total_incomes
        )

        income_2 = IncomeFactory(user=self.user, date=timezone.now())
        expected_total_incomes += income_2.amount

        self.assertEqual(
            self.manager_budget.calculate_monthly_income, expected_total_incomes
        )

    @tag("test")
    def test_check_getting_needs_limit(self):
        expected_limit = self.manager_budget.calculate_monthly_income * (
            self.manager_budget.needs_percentage / 100
        )
        self.assertEqual(self.manager_budget.get_needs_limit, expected_limit)

        IncomeFactory(user=self.user, date=timezone.now())
        expected_limit = self.manager_budget.calculate_monthly_income * (
            self.manager_budget.needs_percentage / 100
        )

        self.assertEqual(self.manager_budget.get_needs_limit, expected_limit)
