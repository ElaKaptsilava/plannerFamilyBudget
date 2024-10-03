from accounts.tests import CustomUserFactory
from budgets_manager import constants
from budgets_manager.models import WantsManager
from budgets_manager.tests.factories.budget_manager_factory import BudgetManagerFactory
from django.test import TestCase
from expenses.tests.factories import ExpenseCategoryFactory, ExpenseFactory
from expenses.types import Type
from incomes.tests.factories import IncomeFactory
from targets.tests.factories import TargetContributionFactory, TargetFactory


class TestWantsManager(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget_manager = BudgetManagerFactory.create(user=self.user)
        self.wants_manager = WantsManager.objects.get(pk=self.budget_manager.pk)

        self.income_amount = 1000
        self.expense_amount = 100
        self.target_contribution_amount = 1000

        self.income = IncomeFactory.create(
            user=self.user, budget=self.budget_manager, amount=self.income_amount
        )
        self.expense_category = ExpenseCategoryFactory.create(
            user=self.user, type=Type.WANTS
        )
        self.expense = ExpenseFactory.create(
            user=self.user,
            budget=self.budget_manager,
            category=self.expense_category,
            amount=self.expense_amount,
        )

        self.target = TargetFactory.create(user=self.user)
        self.target_contribution = TargetContributionFactory.create(
            user=self.user, target=self.target, amount=self.target_contribution_amount
        )

    def test_get_limit(self):
        expected_limit = (
            self.income_amount
            * self.budget_manager.wants_percentage
            / constants.MAX_ALLOCATION
        )
        self.assertEqual(self.wants_manager.get_limit, expected_limit)

    def test_get_progress(self):
        total_spent_in_month = self.wants_manager.total_spent_in_month
        limit = self.wants_manager.get_limit
        expected_progress = (
            total_spent_in_month * constants.MAX_ALLOCATION / limit if limit else 0.0
        )
        self.assertEqual(self.wants_manager.get_progress, expected_progress)

    def test_total_spent_in_month(self):
        total_wants_expenses = self.expense_amount
        total_targets_contribution = self.target_contribution_amount
        expected_total_spent = total_wants_expenses + total_targets_contribution
        self.assertEqual(self.wants_manager.total_spent_in_month, expected_total_spent)

    def test_total_targets_contribution_in_month(self):
        self.assertEqual(
            self.wants_manager.total_targets_contribution_in_month,
            self.target_contribution_amount,
        )

    def test_total_monthly_wants_expenses(self):
        self.assertEqual(
            self.wants_manager.total_monthly_wants_expenses, self.expense_amount
        )

    def test_is_within_wants_budget_true(self):
        self.assertFalse(self.wants_manager.is_within_wants_budget)

    def test_is_within_wants_budget_false(self):
        self.wants_manager.expense_amount = self.wants_manager.get_limit + 1
        self.assertFalse(self.wants_manager.is_within_wants_budget)
