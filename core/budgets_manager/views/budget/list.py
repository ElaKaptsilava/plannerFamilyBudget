from budgets_manager.models import BudgetManager, NeedsManager, WantsManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from targets.models import Saving


class BudgetManagerListView(LoginRequiredMixin, ListView):
    model = BudgetManager
    template_name = "budgets_manager/budget/description.html"

    def get_queryset(self):
        return BudgetManager.objects.select_related("user").get(user=self.request.user)

    def get_context_data(self, **kwargs):
        user = self.request.user

        needs = get_object_or_404(
            NeedsManager.objects.select_related("user"), user=user
        )
        wants = get_object_or_404(
            WantsManager.objects.select_related("user"), user=user
        )
        savings = get_object_or_404(Saving.objects.select_related("user"), user=user)

        kwargs.update({"needs": needs, "wants": wants, "savings": savings})
        return super().get_context_data(**kwargs)
