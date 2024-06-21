from budgets_manager.models import BudgetManager, MonthlyIncomes
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=BudgetManager)
def create_monthly_income(sender, instance, created, **kwargs):
    if created:
        monthly_income, is_exist = MonthlyIncomes.objects.get_or_create(
            budget=instance.budget
        )
        if not is_exist:
            monthly_income.save()
