from budgets_manager.models import MonthlyIncomes
from django.http import JsonResponse
from django.utils import timezone
from django.views import View


class EarningsDataView(View):
    def get(self, request, *args, **kwargs):
        year = timezone.now().year
        budget = request.user.budgetmanager
        earnings = MonthlyIncomes.objects.filter(year=year, budget=budget)
        earns = [0] * 12
        for earning in earnings:
            earns[earning.month - 1] = earning.total_incomes_sum
        data = {
            "data": earns,
        }
        return JsonResponse(data)
