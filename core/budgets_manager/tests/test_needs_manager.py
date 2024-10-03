from accounts.tests import CustomUserFactory
from budgets_manager import constants
from budgets_manager.models import NeedsManager
from budgets_manager.tests.factories.budget_manager_factory import BudgetManagerFactory
from django.test import TestCase
from django.utils import timezone
from expenses.tests.factories import ExpenseCategoryFactory, ExpenseFactory
from expenses.types import Type
from incomes.tests.factories import IncomeFactory
from runningCosts.tests.factories import RunningCostCategoryFactory, RunningCostFactory

from core.constants import labels


class TestNeedsManager(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget_manager = BudgetManagerFactory.create(user=self.user)
        self.needs_manager = NeedsManager.objects.get(pk=self.budget_manager.pk)

        self.income_amount = 1000
        self.expense_amount = 100
        self.cost_amount = 100

        self.income = IncomeFactory.create(
            user=self.user, budget=self.budget_manager, amount=self.income_amount
        )
        self.expense_category = ExpenseCategoryFactory.create(
            user=self.user, type=Type.NEEDS
        )
        self.expense = ExpenseFactory.create(
            user=self.user,
            budget=self.budget_manager,
            category=self.expense_category,
            amount=self.expense_amount,
        )

        self.cost_category = RunningCostCategoryFactory.create(user=self.user)
        self.running_cost = RunningCostFactory.create(
            user=self.user,
            amount=self.cost_amount,
            next_payment_date=timezone.now(),
            category=self.cost_category,
        )

    def test_get_limit(self):
        expected_limit = (
            self.income_amount
            * self.budget_manager.needs_percentage
            / constants.MAX_ALLOCATION
        )
        self.assertEqual(self.needs_manager.get_limit, expected_limit)

    def test_get_progress(self):
        total_spent_in_month = self.needs_manager.total_spent_in_month
        limit = self.needs_manager.get_limit
        expected_progress = (
            total_spent_in_month * constants.MAX_ALLOCATION / limit if limit else 0.0
        )
        self.assertEqual(self.needs_manager.get_progress, expected_progress)

    def test_total_spent_in_month(self):
        total_needs_expenses = self.expense_amount
        total_running_costs = self.running_cost.total_amount_in_month
        expected_total_spent = total_needs_expenses + total_running_costs
        self.assertEqual(self.needs_manager.total_spent_in_month, expected_total_spent)

    def test_total_costs_spent_in_month(self):
        self.assertEqual(
            self.needs_manager.total_costs_spent_in_month,
            self.running_cost.total_amount_in_month,
        )

    def test_total_monthly_needs_expenses(self):
        self.assertEqual(
            self.needs_manager.total_monthly_needs_expenses, self.expense_amount
        )

    def test_is_within_needs_budget_info(self):
        self.assertEqual(self.needs_manager.is_within_needs_budget, labels.INFO)
