from budgets_manager.forms import BudgetManagerForm
from budgets_manager.models import BudgetManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView


class UpdateBudgetView(LoginRequiredMixin, UpdateView):
    form_class = BudgetManagerForm
    template_name = "budgets_manager/budget/budget.html"
    context_object_name = "budget"
    model = BudgetManager
    success_url = reverse_lazy("home")
