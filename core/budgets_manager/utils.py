from django.http import HttpResponse
from django.urls import reverse_lazy


def check_is_user_has_budget(request) -> HttpResponse or None:
    budget_create_url = reverse_lazy("manager:budget-list-create")
    if not hasattr(request.user, "budgetmanager") and request.path != budget_create_url:
        return budget_create_url
