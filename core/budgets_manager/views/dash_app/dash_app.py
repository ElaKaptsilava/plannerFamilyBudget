import secrets
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Union

from budgets_manager.models import MonthlyIncomes
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from incomes.models import Income


class EarningsDataView(View):
    def get(self, request, *args, **kwargs) -> JsonResponse:
        year = timezone.now().year
        budget = request.user.set_budget.budget
        earnings = MonthlyIncomes.objects.filter(year=year, budget=budget)
        earns = [0] * 12
        for earning in earnings:
            earns[earning.month - 1] = earning.total_incomes_sum

        return JsonResponse({"data": earns})


class RevenueSourcesView(View):
    def get(self, request, *args, **kwargs) -> JsonResponse:
        current = timezone.now()
        last_of_previous_month = self.calculate_previous_month(
            current.month, current.year
        )
        incomes = Income.objects.filter(
            date__year=last_of_previous_month[0],
            date__month=last_of_previous_month[1],
            user=request.user,
        ).order_by("-amount")

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

    @staticmethod
    def calculate_previous_month(
        current_month: int, current_year: int
    ) -> Union[str, str]:
        first_of_current_month = datetime(current_year, current_month, 1)
        last_of_previous_month = first_of_current_month - timedelta(
            days=1
        )  # pip install python-dateutil
        return last_of_previous_month.year, last_of_previous_month.month
