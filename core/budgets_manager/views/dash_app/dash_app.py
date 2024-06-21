from budgets_manager.models import MonthlyIncomes
from django.http import JsonResponse
from django.utils import timezone
from django.views import View


class EarningsDataView(View):
    def get(self, request, *args, **kwargs):
        year = timezone.now().year
        month = timezone.now().month
        budget = request.user.budgetmanager
        earnings = MonthlyIncomes.objects.filter(year=year, budget=budget)
        earns = [0] * 12
        for earning in earnings:
            earns[earning.month - 1] = earning.amount
        earns[month - 1] = budget.calculate_monthly_incomes
        data = {
            "data": earns,
        }
        return JsonResponse(data)
