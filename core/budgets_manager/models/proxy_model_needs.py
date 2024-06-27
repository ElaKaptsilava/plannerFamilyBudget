from budgets_manager.models import BudgetManager
from django.utils import timezone
from runningCosts.models import RunningCost


class NeedsManager(BudgetManager):
    class Meta:
        proxy = True

    @property
    def get_needs_limit(self):
        return self.calculate_monthly_incomes * float(self.needs_percentage / 100)

    @property
    def total_needs_amount_in_month(self):
        current_month = timezone.now().month
        current_year = timezone.now().year

        filtered_running_costs = RunningCost.objects.filter(
            user=self.user,
            next_payment_date__month=current_month,
            next_payment_date__year=current_year,
        )

        total_cost = sum(
            map(lambda item: item.total_amount_in_month, filtered_running_costs)
        )

        return total_cost

    @property
    def is_within_needs_budget(self):
        total_needs_amount_in_month_percentage = (
            self.total_needs_amount_in_month * 100 / self.get_needs_limit
        )
        if total_needs_amount_in_month_percentage <= 80:
            return [
                ("border-left-success", "text-success"),
            ]
        elif total_needs_amount_in_month_percentage < 100:
            return [
                ("border-right-warning", "text-warning"),
            ]
        return [
            ("border-left-danger", "text-danger"),
        ]
