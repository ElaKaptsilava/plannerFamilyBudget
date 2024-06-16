from accounts.factories import CustomUserFactory
from budgets_manager.models import NeedsManager
from budgets_manager.tests.factories import BudgetManagerFactory
from django.test import TestCase
from django.utils import timezone
from expenses.tests.factories import ExpenseCategoryFactory, ExpenseFactory
from incomes.tests.factories import IncomeFactory
from runningCosts.tests.factories import RunningCostCategoryFactory, RunningCostFactory


class NeedsLimitTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory()
        self.manager_budget = BudgetManagerFactory(user=self.user)
        self.expenses_category = ExpenseCategoryFactory(user=self.user)
        self.running_cost_category = RunningCostCategoryFactory(user=self.user)
        self.incomes = IncomeFactory(user=self.user, date=timezone.now())
        self.needs_manager = NeedsManager.objects.get(user=self.user)

    def test_calculate_monthly_income_when_user_add_more_incomes(self):
        self.assertEqual(
            self.needs_manager.calculate_monthly_income, self.incomes.amount
        )

        income_1 = IncomeFactory(user=self.user, date=timezone.now())
        expected_total_incomes = self.incomes.amount + income_1.amount

        self.assertEqual(
            self.needs_manager.calculate_monthly_income, expected_total_incomes
        )

        income_2 = IncomeFactory(user=self.user, date=timezone.now())
        expected_total_incomes += income_2.amount

        self.assertEqual(
            self.needs_manager.calculate_monthly_income, expected_total_incomes
        )

    def test_check_getting_needs_limit(self):
        expected_limit = self.needs_manager.calculate_monthly_income * (
            float(self.needs_manager.needs_percentage) / 100
        )
        self.assertEqual(self.needs_manager.get_needs_limit, expected_limit)

        IncomeFactory(user=self.user, date=timezone.now())
        expected_limit = self.needs_manager.calculate_monthly_income * (
            float(self.needs_manager.needs_percentage) / 100
        )

        self.assertEqual(self.needs_manager.get_needs_limit, expected_limit)

    def tests_total_needs_expenses_when_user_add_more_expenses(self):
        expenses = ExpenseFactory.create(
            user=self.user, category=self.expenses_category, datetime=timezone.now()
        )
        self.assertEqual(self.needs_manager.total_needs_expenses, expenses.amount)

        cost = RunningCostFactory.create(
            user=self.user, category=self.running_cost_category
        )
        expected_total_needs_expenses = cost.amount + expenses.amount

        self.assertEqual(
            self.needs_manager.total_needs_expenses, expected_total_needs_expenses
        )

        next_payment_date = timezone.now() + timezone.timedelta(days=60)

        RunningCostFactory.create(
            user=self.user,
            category=self.running_cost_category,
            next_payment_date=next_payment_date,
        )

        self.assertEqual(
            self.needs_manager.total_needs_expenses, expected_total_needs_expenses
        )

    def test_is_within_needs_budget(self):
        expenses = ExpenseFactory.create(
            user=self.user,
            category=self.expenses_category,
            datetime=timezone.now(),
            amount=10,
        )
        self.assertTrue(self.needs_manager.is_within_needs_budget)

        expenses.amount += self.needs_manager.calculate_monthly_income
        expenses.save()

        self.assertFalse(self.needs_manager.is_within_needs_budget)
