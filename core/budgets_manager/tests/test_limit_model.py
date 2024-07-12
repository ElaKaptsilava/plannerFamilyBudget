from accounts.tests import CustomUserFactory
from budgets_manager.models import LimitManager
from budgets_manager.tests import BudgetManagerFactory, LimitManagerFactory
from django.core.exceptions import ValidationError
from django.test import TestCase
from expenses import types
from expenses.tests.factories import ExpenseCategoryFactory, ExpenseFactory
from incomes.tests.factories import IncomeFactory
from runningCosts.tests.factories import RunningCostCategoryFactory, RunningCostFactory
from targets.tests import TargetContributionFactory, TargetFactory


class TestLimitModel(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budgetmanager = BudgetManagerFactory.create(user=self.user)
        self.income = IncomeFactory.create(user=self.user)
        self.expense_category = ExpenseCategoryFactory.create(user=self.user)
        self.category_running_cost = RunningCostCategoryFactory.create(user=self.user)
        self.target = TargetFactory.create(user=self.user)

        self.target_limit = LimitManagerFactory.create(
            budget_manager=self.budgetmanager,
            target=self.target,
            type=types.Type.WANTS,
            amount=100,
        )
        self.cost_limit = LimitManagerFactory.create(
            budget_manager=self.budgetmanager,
            category_running_cost=self.category_running_cost,
            type=types.Type.NEEDS,
            amount=100,
        )
        self.expense_limit = LimitManagerFactory.create(
            budget_manager=self.budgetmanager,
            category_expense=self.expense_category,
            type=types.Type.NEEDS,
            amount=100,
        )

    def test_calculate_target_spent_in_month(self):
        """
        ...
        """
        contribution = TargetContributionFactory.create(
            user=self.user, target=self.target
        )
        spent = contribution.amount

        get_limit = LimitManager.objects.get(
            budget_manager=self.budgetmanager, target=self.target
        )

        self.assertEqual(get_limit.calculate_total_spent(), spent)

        contribution1 = TargetContributionFactory.create(
            user=self.user, target=self.target
        )

        spent += contribution1.amount

        self.assertEqual(get_limit.calculate_total_spent(), spent)

    def test_calculate_cost_spent_in_month(self):
        cost = RunningCostFactory(user=self.user, category=self.category_running_cost)
        spent = cost.total_amount_in_month

        self.assertEqual(
            self.cost_limit.calculate_total_spent(), cost.total_amount_in_month
        )

        cost = RunningCostFactory(
            user=self.user, category=self.category_running_cost, period=2
        )
        spent += cost.total_amount_in_month

        self.assertEqual(self.cost_limit.calculate_total_spent(), spent)

    def test_calculate_expenses_spent_in_month(self):
        expense = ExpenseFactory.create(user=self.user, category=self.expense_category)
        spent = expense.amount

        self.assertEqual(self.expense_limit.calculate_total_spent(), spent)

    def test_amount_within_limit(self):
        TargetContributionFactory.create(
            user=self.user, target=self.target, amount=self.target_limit.amount - 1
        )

        self.assertTrue(self.target_limit.within_limit)

    def test_validation_error_when_amount_greate_the_limit(self):
        with self.assertRaises(ValidationError):
            ExpenseFactory.create(
                user=self.user,
                category=self.expense_category,
                amount=self.income.amount,
            )
