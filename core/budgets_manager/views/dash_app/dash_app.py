import secrets
from collections import defaultdict

from budgets_manager.models import MonthlyIncomes
from django.http import JsonResponse
from django.utils import timezone
from django.views import View


class EarningsDataView(View):
    def get(self, request, *args, **kwargs) -> JsonResponse:
        year = timezone.now().year
        budget = request.user.set_budget.budget
        earnings = MonthlyIncomes.objects.filter(year=year, budget=budget)
        earns = [0] * 12
        for earning in earnings:
            earns[earning.month - 1] = earning.total_incomes

        return JsonResponse({"data": earns})


class RevenueSourcesView(View):
    def get(self, request, *args, **kwargs) -> JsonResponse:
        incomes = request.user.set_budget.budget.get_monthly_incomes().order_by(
            "-amount"
        )

        data = defaultdict(list)
        labels = defaultdict(float)

        for income in incomes:
            labels[income.source] += float(income.amount)

        data["labels"] = list(labels.keys())
        data["amounts"] = list(labels.values())

        while len(data["colors"]) < len(data["labels"]):
            color = self.generate_random_color()
            if color not in data["colors"]:
                data["colors"].append(color)

        return JsonResponse(dict(data))

    @staticmethod
    def generate_random_color() -> str:
        return "#{:06x}".format(secrets.randbelow(0xFFFFFF))
