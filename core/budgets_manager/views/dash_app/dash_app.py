from budgets_manager.models import MonthlyIncomes
from django.http import JsonResponse
from django.utils import timezone


def earnings_data(request):
    year = timezone.now().year
    month = timezone.now().month
    budget = request.user.budgetmanager
    earnings = MonthlyIncomes.objects.filter(year=year, budget=budget)
    print(earnings)
    earns = [0] * 12
    for earning in earnings:
        earns.insert(earning.month - 1, earning.amount)
    earns.insert(month - 1, budget.calculate_monthly_incomes)
    print(earns)
    data = {
        "data": earns,
    }
    return JsonResponse(data)
