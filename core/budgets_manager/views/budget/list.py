from budgets_manager.models import BudgetManager, NeedsManager, WantsManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class BudgetManagerListView(LoginRequiredMixin, ListView):
    model = BudgetManager
    template_name = "budgets_manager/budget/description.html"

    def get_queryset(self):
        print(self.model.objects.all())
        return (
            self.model.objects.select_related("user")
            .filter(user=self.request.user)
            .prefetch_related("expense", "category_running_cost", "target", "income")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["budget"] = self.get_queryset()
        context["needs"] = WantsManager.objects.get(user=self.request.user)
        context["saves"] = NeedsManager.objects.get(user=self.request.user)
        return context
