from budgets_manager.models import BudgetManager, NeedsManager, WantsManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView


class BudgetManagerListView(LoginRequiredMixin, ListView):
    model = BudgetManager
    template_name = "budgets_manager/budget/description.html"

    def get_queryset(self):
        return BudgetManager.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["needs"] = get_object_or_404(
            NeedsManager.objects.select_related("user"), user=self.request.user
        )
        context["wants"] = get_object_or_404(
            WantsManager.objects.select_related("user"), user=self.request.user
        )
        return context
