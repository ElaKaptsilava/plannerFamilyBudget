from accounts.models import CustomUser
from budgets_manager.models import BudgetManager, NeedsManager, SavingManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class HomeView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name: str = "accounts/dashboard.html"
    http_method_names: list = ["get"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["budget"] = BudgetManager.objects.get(user=self.request.user)
        context["needs"] = NeedsManager.objects.get(user=self.request.user)
        context["saves"] = SavingManager.objects.get(user=self.request.user)
        return context
