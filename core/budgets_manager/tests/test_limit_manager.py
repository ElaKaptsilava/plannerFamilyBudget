from accounts.tests import CustomUserFactory
from budgets_manager.tests.factories.budget_manager_factory import BudgetManagerFactory
from budgets_manager.tests.factories.limit_manager_factory import LimitManagerFactory
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from expenses.tests.factories import ExpenseCategoryFactory, ExpenseFactory
from expenses.types import Type
from incomes.tests.factories import IncomeFactory
from targets.tests.factories import TargetFactory


class TestLimitManager(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget_manager = BudgetManagerFactory.create(user=self.user)
        self.expense_category = ExpenseCategoryFactory.create(
            user=self.user, type=Type.WANTS
        )

        self.income_amount = 10000
        self.expense_amount = 100
        self.target_contribution_amount = 1000
        self.limit_amount = 500
        self.income = IncomeFactory.create(
            user=self.user, budget=self.budget_manager, amount=self.income_amount
        )

        self.limit_manager = LimitManagerFactory.create(
            budget_manager=self.budget_manager,
            category_expense=self.expense_category,
            amount=self.limit_amount,
            type=Type.WANTS,
        )

        self.expense = ExpenseFactory.create(
            user=self.user,
            budget=self.budget_manager,
            category=self.expense_category,
            amount=self.expense_amount,
        )
        self.target = TargetFactory.create(
            user=self.user,
            amount=1000,
            deadline=timezone.now() + timezone.timedelta(days=300),
        )

    def test_validate_budget_type_invalid(self):
        """Test invalid budget type combinations (e.g., NEEDS type with target)."""
        with self.assertRaises(ValidationError) as context:
            LimitManagerFactory.create(
                budget_manager=self.budget_manager,
                type=Type.NEEDS,
                target=self.target,
                amount=self.limit_amount,
            )

        self.assertIn(
            "For 'needs' type, either category expense or category running cost must be set.",
            str(context.exception),
        )

    def test_valid_needs_with_category_expense(self):
        """Test valid NEEDS type with category_expense."""
        expense_category = ExpenseCategoryFactory.create(
            user=self.user, type=Type.WANTS
        )
        limit_manager = LimitManagerFactory.create(
            budget_manager=self.budget_manager,
            type=Type.WANTS,
            category_expense=expense_category,
            amount=self.limit_amount,
        )
        self.assertEqual(limit_manager.amount, self.limit_amount)
        self.assertTrue(limit_manager)
