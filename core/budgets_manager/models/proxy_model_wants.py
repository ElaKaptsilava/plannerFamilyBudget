from budgets_manager import constants
from budgets_manager.models import BudgetManager
from django.db import models
from expenses.types import Type
from targets.models import TargetContribution

from core.constants import labels


class WantsManager(BudgetManager):
    class Meta:
        proxy = True

    @property
    def get_limit(self) -> float:
        return self.total_monthly_incomes * float(
            self.wants_percentage / constants.MAX_ALLOCATION
        )

    @property
    def get_progress(self) -> float:
        if not self.get_limit:
            return 0
        return self.total_spent_in_month * constants.MAX_ALLOCATION / self.get_limit

    @property
    def total_spent_in_month(self) -> float:
        return (
            self.total_targets_contribution_in_month + self.total_monthly_wants_expenses
        )

    @property
    def total_targets_contribution_in_month(self) -> float:
        get_queryset = TargetContribution.objects.prefetch_related("user").order_by(
            "user", "date"
        )

        targets = get_queryset.filter(
            user=self.user, date__range=self.get_month_range()
        )
        total = targets.aggregate(total=models.Sum("amount"))["total"]
        if not total:
            return 0.0
        return float(total)

    @property
    def total_monthly_wants_expenses(self) -> float:
        expenses_wants = self.get_monthly_expenses().filter(
            category__type=Type.WANTS,
        )
        total = expenses_wants.aggregate(total=models.Sum("amount"))["total"]
        return float(total) if total else 0.0

    @property
    def is_within_wants_budget(self) -> bool:
        return self.total_spent_in_month <= self.get_limit

    @property
    def is_within_wants_budget_label(self):
        if self.get_progress <= constants.WARNING_THRESHOLD:
            return labels.INFO
        elif self.get_progress < constants.DANGER_THRESHOLD:
            return labels.WARNING
        return labels.DANGER
