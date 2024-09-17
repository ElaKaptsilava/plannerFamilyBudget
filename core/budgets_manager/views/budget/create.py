from budgets_manager.forms.limit import BudgetManagerForm
from budgets_manager.models import BudgetManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView


class BudgetManagerCreateView(LoginRequiredMixin, CreateView):
    form_class = BudgetManagerForm
    template_name = "budgets_manager/budget/budget-create.html"
    context_object_name = "budget"
    model = BudgetManager
    success_url = reverse_lazy("subscription:list-create")

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        response = super().form_valid(form)
        form.instance.participants.add(self.request.user)
        return response
