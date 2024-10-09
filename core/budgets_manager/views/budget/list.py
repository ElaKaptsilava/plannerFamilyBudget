from budgets_manager.models import BudgetManager, NeedsManager, SetBudget, WantsManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from targets.models import Saving


class BudgetManagerDetailView(LoginRequiredMixin, DetailView):
    model = BudgetManager
    template_name = "budgets_manager/budget/description.html"
    context_object_name = "budget_manager"

    def get_object(self, queryset=None):
        set_budget = get_object_or_404(SetBudget, pk=self.kwargs["pk"])
        return set_budget.budget

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        needs = NeedsManager.objects.get(pk=self.get_object().pk)
        wants = WantsManager.objects.get(pk=self.get_object().pk)
        savings = Saving.objects.get(user=self.get_object().user)
        context.update({"needs": needs, "wants": wants, "savings": savings})
        return context
