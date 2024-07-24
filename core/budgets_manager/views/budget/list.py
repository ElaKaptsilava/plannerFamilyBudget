from budgets_manager.models import BudgetManager, NeedsManager, WantsManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from targets.models import Saving


class BudgetManagerListView(LoginRequiredMixin, ListView):
    model = BudgetManager
    template_name = "budgets_manager/budget/description.html"

    def get_queryset(self):
        return BudgetManager.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        kwargs["needs"] = get_object_or_404(
            NeedsManager.objects.select_related("user"), user=self.request.user
        )
        kwargs["wants"] = get_object_or_404(
            WantsManager.objects.select_related("user"), user=self.request.user
        )
        kwargs["savings"] = get_object_or_404(
            Saving.objects.select_related("user"), user=self.request.user
        )
        return super().get_context_data(**kwargs)
