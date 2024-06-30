from django.shortcuts import redirect
from django.urls import reverse_lazy


class BudgetCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            budget_create_url = reverse_lazy(
                "manager:budget-list-create", kwargs={"user_id": request.user.pk}
            )
            if (
                not hasattr(request.user, "budgetmanager")
                and request.path != budget_create_url
            ):
                return redirect(budget_create_url)

        response = self.get_response(request)
        return response


def redirect_to_budget_create_view_if_budget_not_created(request):
    if request.user.is_authenticated:
        budget_create_url = reverse_lazy(
            "manager:budget-list-create", kwargs={"user_id": request.user.pk}
        )
        if (
            not hasattr(request.user, "budgetmanager")
            and request.path != budget_create_url
        ):
            return redirect(budget_create_url)
