from budgets_manager.forms.set_budget import SetBudgetForm
from budgets_manager.models import SetBudget
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView


class SetBudgetView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SetBudget
    form_class = SetBudgetForm
    success_message = "Updated budget successfully!"
    success_url = reverse_lazy("home")
    template_name = "budgets_manager/budget/budget.html"
    context_object_name = "set_budget"
