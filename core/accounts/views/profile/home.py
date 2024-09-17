from accounts.models import CustomUser
from budgets_manager.models import BudgetManager, NeedsManager, WantsManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from multi_user.models import FamilyBudget
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
                "family_budget": self.get_family_budgets_object(user),
                "needs": self.get_needs_manager_object_or_404(user),
                "wants": self.get_wants_manager_object_or_404(user),
                "savings": self.get_savings_object_or_404(user),
                "positive_form": SavingPositiveContributionsForm(),
                "negative_form": SavingNegativeContributionsForm(),
            }
        )
        print(self.get_family_budgets_object(user), "family")
        return super().get_context_data(**kwargs)

    @staticmethod
    def get_budget_object(user: CustomUser) -> BudgetManager:
        return user.set_budget.budget

    @staticmethod
    def get_needs_manager_object_or_404(user: CustomUser) -> NeedsManager:
        return get_object_or_404(NeedsManager.objects.select_related("user"), user=user)

    @staticmethod
    def get_wants_manager_object_or_404(user: CustomUser) -> WantsManager:
        return get_object_or_404(WantsManager.objects.select_related("user"), user=user)

    @staticmethod
    def get_savings_object_or_404(user: CustomUser) -> Saving:
        return get_object_or_404(Saving.objects.select_related("user"), user=user)

    @staticmethod
    def get_family_budgets_object(user: CustomUser) -> QuerySet[FamilyBudget]:
        try:
            family_budget = FamilyBudget.objects.get(budget_manager=user.budgetmanager)
        except Exception:
            return None
        return family_budget
