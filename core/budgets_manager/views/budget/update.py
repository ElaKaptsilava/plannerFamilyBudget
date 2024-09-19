from budgets_manager.forms.limit import BudgetManagerForm
from budgets_manager.models import BudgetManager
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView


class UpdateBudgetView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = BudgetManagerForm
    template_name = "budgets_manager/budget/budget.html"
    context_object_name = "budget"
    model = BudgetManager
    success_url = reverse_lazy("home")
    success_message = "Budget updated successfully!"

    def form_invalid(self, form):
        messages.info(self.request, "Check budget data!")
        return super().form_invalid(form)
