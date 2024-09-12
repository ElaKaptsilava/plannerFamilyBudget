from budgets_manager.models import BudgetManager, MonthlyIncomes
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from multi_user.models import FamilyBudget


@receiver(post_save, sender=BudgetManager)
def create_monthly_income(sender, instance, created, **kwargs):
    year = timezone.now().year
    month = timezone.now().month
    if created:
        monthly_income, is_exist = MonthlyIncomes.objects.get_or_create(
            budget=instance, year=year, month=month
        )
        monthly_income.save()
        if not FamilyBudget.objects.filter(
            owner=instance.user, budget_manager=instance
        ).exists():
            budget = FamilyBudget.objects.create(
                owner=instance.user, budget_manager=instance
            )
            budget.members.add(instance.user)
            budget.save()
