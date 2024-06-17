from budgets_manager.models import BudgetManager
from django.utils import timezone
from targets.models import Target


class WantsManager(BudgetManager):
    class Meta:
        proxy = True

    @property
    def get_wants_limit(self):
        return self.calculate_monthly_income * float(self.wants_percentage / 100)

    @property
    def total_wants_expenses(self):
        targets = Target.objects.filter(deadline__lte=timezone.now().date())
        total_monthly_payment = sum(
            target.monthly_payment for target in targets if not target.is_completed
        )
        return total_monthly_payment
