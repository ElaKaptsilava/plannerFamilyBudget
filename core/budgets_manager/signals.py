from budgets_manager.models import BudgetManager, MonthlyIncomes
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(post_save, sender=BudgetManager)
def create_monthly_income(sender, instance, created, **kwargs):
    year = timezone.now().year
    month = timezone.now().month
    if created and instance.user.profile_created:
        monthly_income, is_exist = MonthlyIncomes.objects.get_or_create(
            budget=instance.budget, year=year, month=month
        )
        monthly_income.save()
