from budgets_manager.models import BudgetManager
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from incomes.models import Income


@receiver(post_save, sender=Income)
@receiver(post_delete, sender=Income)
def update_budget_manager_monthly_income(sender, instance, created, **kwargs):
    """
    Signal receiver to update BudgetManager's monthly_income whenever a new Income is added.
    """
    if created:
        budget_manager = BudgetManager.objects.get_or_create(user=instance.user)[0]
        budget_manager.update_monthly_income()
