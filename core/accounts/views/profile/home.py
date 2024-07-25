from budgets_manager.models import BudgetManager, NeedsManager, WantsManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from targets.forms import (
    SavingNegativeContributionsForm,
    SavingPositiveContributionsForm,
)
from targets.models import Saving


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        user = self.request.user

        kwargs.update(
            {
                "budget": self.get_budget_object(user),
                "needs": self.get_needs_manager_object_or_404(user),
                "wants": self.get_wants_manager_object_or_404(user),
                "savings": self.get_savings_object_or_404(user),
                "positive_form": SavingPositiveContributionsForm(),
                "negative_form": SavingNegativeContributionsForm(),
            }
        )
        return super().get_context_data(**kwargs)

    @staticmethod
    def get_budget_object(user) -> BudgetManager:
        return user.budgetmanager

    @staticmethod
    def get_needs_manager_object_or_404(user) -> NeedsManager:
        return get_object_or_404(NeedsManager.objects.select_related("user"), user=user)

    @staticmethod
    def get_wants_manager_object_or_404(user) -> WantsManager:
        return get_object_or_404(WantsManager.objects.select_related("user"), user=user)

    @staticmethod
    def get_savings_object_or_404(user) -> Saving:
        return get_object_or_404(Saving.objects.select_related("user"), user=user)
