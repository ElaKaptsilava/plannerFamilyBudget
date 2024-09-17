from budgets_manager.models import BudgetManager
from django.http import HttpResponse
from django.urls import reverse_lazy


def check_is_user_has_budget(request) -> HttpResponse or None:
    budget_create_url = reverse_lazy("manager:budget-list-create")
    is_budget = BudgetManager.objects.filter(user=request.user).exists()
    if not is_budget and request.path != budget_create_url:
        return budget_create_url
