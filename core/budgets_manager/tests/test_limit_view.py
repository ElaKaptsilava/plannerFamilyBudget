from accounts.tests import CustomUserFactory
from budgets_manager.tests.factories import BudgetManagerFactory
from django.test import TestCase
from django.urls import reverse_lazy
from expenses import types
from expenses.tests.factories import ExpenseCategoryFactory
from incomes.tests.factories import IncomeFactory
from runningCosts.tests.factories import RunningCostCategoryFactory
from targets.tests import TargetFactory


class LimitViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budgetmanager = BudgetManagerFactory.create(user=self.user)
        self.income = IncomeFactory.create(user=self.user)
        self.category_expense = ExpenseCategoryFactory.create(user=self.user)
        self.category_running_cost = RunningCostCategoryFactory.create(user=self.user)
        self.target = TargetFactory.create(user=self.user)

        self.limit_create = reverse_lazy("manager:limits-list-create")
        self.limit_delete = reverse_lazy("manager:limits-delete-multiple")
        self.limit_update = reverse_lazy(
            "manager:limits-detail-update", kwargs={"pk": self.limit.pk}
        )

        self.clean_data_cost = {
            "type": types.Type.NEEDS,
            "category_running_cost": self.category_running_cost.pk,
            "amount": 1,
        }
        self.clean_data_target = {
            "type": types.Type.WANTS,
            "target": self.target.pk,
            "amount": self.income.amount,
        }
        self.clean_data_expense = {
            "type": self.category_expense.type,
            "category_expense": self.category_expense.pk,
            "amount": 1,
        }
