from accounts.models import CustomUser
from budgets_manager.models import BudgetManager, NeedsManager, WantsManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from expenses.models import Expense, ExpenseCategory
from incomes.models import Income
from runningCosts.models import RunningCost
from targets.forms import SavingContributionsForm
from targets.models import Saving, Target


class HomeView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name: str = "accounts/dashboard.html"
    http_method_names: list = ["get"]

    def get_queryset(self):
        expenses_prefetch = Prefetch(
            "expenses",
            queryset=Expense.objects.only("id", "amount", "date", "category"),
        )
        expense_categories_prefetch = Prefetch(
            "expense_categories", queryset=ExpenseCategory.objects.only("id", "name")
        )
        running_costs_prefetch = Prefetch(
            "running_costs",
            queryset=RunningCost.objects.only(
                "id", "name", "amount", "next_pyment_date"
            ),
        )
        targets_prefetch = Prefetch(
            "targets", queryset=Target.objects.only("id", "name", "amount")
        )
        incomes_prefetch = Prefetch(
            "incomes", queryset=Income.objects.only("id", "amount", "date", "source")
        )

        queryset = CustomUser.objects.prefetch_related(
            expenses_prefetch,
            expense_categories_prefetch,
            running_costs_prefetch,
            targets_prefetch,
            incomes_prefetch,
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["budget"] = get_object_or_404(
            BudgetManager.objects.select_related("user"), user=self.request.user
        )
        context["needs"] = get_object_or_404(
            NeedsManager.objects.select_related("user"), user=self.request.user
        )
        context["wants"] = get_object_or_404(
            WantsManager.objects.select_related("user"), user=self.request.user
        )
        context["savings"] = get_object_or_404(
            Saving.objects.select_related("user"), user=self.request.user
        )
        context["saving_contribution"] = SavingContributionsForm()
        return context
