from budgets_manager.models import BudgetManager
from django.utils import timezone
from expenses.models import Expense
from runningCosts.models import RunningCost


class NeedsManager(BudgetManager):
    class Meta:
        proxy = True

    @property
    def get_needs_limit(self):
        return self.calculate_monthly_income * float(self.needs_percentage / 100)

    @property
    def total_needs_expenses(self):
        current_month = timezone.now().month
        current_year = timezone.now().year

        filtered_running_costs = RunningCost.objects.filter(
            user=self.user,
            next_payment_date__month=current_month,
            next_payment_date__year=current_year,
        )
        filtered_expenses = Expense.objects.filter(
            user=self.user,
            datetime__month=current_month,
            datetime__year=current_year,
        )

        total_cost = sum(
            map(lambda item: item.total_amount_in_month, filtered_running_costs)
        )
        total_expenses = sum(map(lambda item: item.amount, filtered_expenses))

        return total_cost + total_expenses

    @property
    def is_within_needs_budget(self):
        return self.total_needs_expenses <= self.get_needs_limit
