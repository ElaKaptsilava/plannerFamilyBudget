from budgets_manager.models import BudgetManager, NeedsManager, SavingManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class BudgetManagerListView(LoginRequiredMixin, ListView):
    model = BudgetManager
    template_name = "budgets_manager/budget/description.html"

    def get_queryset(self):
        return self.model.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["budget"] = self.get_queryset()
        context["needs"] = SavingManager.objects.get(user=self.request.user)
        context["saves"] = NeedsManager.objects.get(user=self.request.user)
        return context
