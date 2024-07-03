from budgets_manager import constants
from budgets_manager.models import BudgetManager
from targets.models import Target

from core.constants import labels


class WantsManager(BudgetManager):
    class Meta:
        proxy = True

    @property
    def get_wants_limit(self) -> float:
        return self.calculate_total_monthly_incomes * float(
            self.savings_percentage / constants.MAX_ALLOCATION
        )

    @property
    def get_targets_progress(self) -> float:
        return (
            self.total_targets_amount_in_month
            * constants.MAX_ALLOCATION
            / self.get_wants_limit
        )

    @property
    def total_targets_amount_in_month(self):
        targets = Target.objects.filter(user=self.user)
        monthly_payment_list = map(lambda target: target.monthly_payment, targets)
        return sum(monthly_payment_list)

    @property
    def is_within_wants_budget(self):
        return self.total_targets_amount_in_month <= self.get_wants_limit

    @property
    def is_within_wants_budget_label(self):
        if self.get_targets_progress <= constants.WARNING_THRESHOLD:
            return labels.INFO
        elif self.get_targets_progress < constants.DANGER_THRESHOLD:
            return labels.WARNING
        return labels.DANGER
