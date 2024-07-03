from budgets_manager import constants
from budgets_manager.models import BudgetManager
from runningCosts.models import RunningCost

from core.constants import labels


class NeedsManager(BudgetManager):
    class Meta:
        proxy = True

    @property
    def get_needs_limit(self) -> float:
        return (
            self.calculate_total_monthly_incomes
            * float(self.needs_percentage)
            / constants.MAX_ALLOCATION
        )

    @property
    def get_needs_progress(self) -> float:
        return (
            self.total_needs_amount_in_month
            * constants.MAX_ALLOCATION
            / self.get_needs_limit
            or 0.0
        )

    @property
    def total_needs_amount_in_month(self) -> float:
        filtered_running_costs = RunningCost.objects.filter(
            user=self.user,
            next_payment_date__month=self.TODAY.month,
            next_payment_date__year=self.TODAY.year,
        )
        total_amounts_in_month = map(
            lambda item: float(item.total_amount_in_month), filtered_running_costs
        )
        return sum(total_amounts_in_month)

    @property
    def is_within_needs_budget(self):
        if self.get_needs_progress <= constants.WARNING_THRESHOLD:
            return labels.INFO
        elif self.get_needs_progress < constants.DANGER_THRESHOLD:
            return labels.WARNING
        return labels.DANGER
