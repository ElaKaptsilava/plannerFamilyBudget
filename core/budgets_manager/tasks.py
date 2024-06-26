from budgets_manager.models import BudgetManager, MonthlyIncomes
from celery import shared_task
from django.utils import timezone


@shared_task
def create_monthly_incomes_modal():
    current_month = timezone.now().month
    current_year = timezone.now().year

    budgets = BudgetManager.objects.all()

    for budget in budgets:
        monthly_entry, created = MonthlyIncomes.objects.get_or_create(
            budget=budget,
            year=current_year,
            month=current_month,
        )

        if not created:
            monthly_entry.total_income = budget.calculate_monthly_incomes
            monthly_entry.save()

    return f"Monthly incomes updated for {current_year}-{current_month}."
