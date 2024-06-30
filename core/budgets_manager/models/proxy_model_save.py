from budgets_manager.models import BudgetManager
from targets.models import Target


class SavingManager(BudgetManager):
    class Meta:
        proxy = True

    @property
    def get_saving_limit(self):
        return float(self.calculate_monthly_incomes) * float(
            self.savings_percentage / 100
        )

    @property
    def total_targets_amount_in_month(self):
        targets = Target.objects.filter(user=self.user)
        monthly_payment_list = map(lambda target: target.monthly_payment, targets)
        return sum(monthly_payment_list)

    @property
    def is_within_saving_budget(self):
        return self.total_targets_amount_in_month <= self.get_saving_limit
