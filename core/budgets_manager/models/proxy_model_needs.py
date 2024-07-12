from budgets_manager import constants
from budgets_manager.models import BudgetManager
from django.db import models
from expenses.models import Expense
from expenses.types import Type
from runningCosts.models import RunningCost

from core.constants import labels


class NeedsManager(BudgetManager):
    class Meta:
        proxy = True

    @property
    def get_limit(self) -> float:
        return (
            self.calculate_total_monthly_incomes
            * float(self.needs_percentage)
            / constants.MAX_ALLOCATION
        )

    @property
    def get_progress(self) -> float:
        return (
            self.total_spent_in_month * constants.MAX_ALLOCATION / self.get_limit or 0.0
        )

    @property
    def total_spent_in_month(self) -> float:
        return self.total_expenses_spent_in_month + self.total_costs_spent_in_month

    @property
    def total_costs_spent_in_month(self) -> float:
        filtered_running_costs = RunningCost.objects.filter(
            user=self.user,
            next_payment_date__month=self.TODAY.month,
            next_payment_date__year=self.TODAY.year,
        ).order_by("next_payment_date")
        if not filtered_running_costs:
            return 0.0
        total_amounts_in_month = map(
            lambda item: float(item.total_amount_in_month), filtered_running_costs
        )
        return sum(total_amounts_in_month)

    @property
    def total_expenses_spent_in_month(self) -> float:
        queryset = Expense.objects.prefetch_related("category", "user")
        if not queryset:
            return 0.0
        expenses_wants = queryset.filter(
            user=self.user,
            datetime__month=self.TODAY.month,
            datetime__year=self.TODAY.year,
            category__type=Type.NEEDS,
        )
        total = expenses_wants.aggregate(total=models.Sum("amount"))["total"] or 0.0
        return float(total)

    @property
    def is_within_needs_budget(self) -> str:
        if self.get_progress <= constants.WARNING_THRESHOLD:
            return labels.INFO
        elif self.get_progress < constants.DANGER_THRESHOLD:
            return labels.WARNING
        return labels.DANGER
