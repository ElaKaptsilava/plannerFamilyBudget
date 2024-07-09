from django.shortcuts import redirect
from django.urls import reverse_lazy


def check_and_redirect_to_budget_create(request):
    if request.user.is_authenticated:
        budget_create_url = reverse_lazy("manager:budget-list-create")
        if (
            not hasattr(request.user, "budgetmanager")
            and request.path != budget_create_url
        ):
            return redirect(budget_create_url)
