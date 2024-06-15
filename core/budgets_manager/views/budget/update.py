from budgets_manager.forms import BudgetManagerForm
from budgets_manager.models import BudgetManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView


class UpdateBudgetView(LoginRequiredMixin, UpdateView):
    form_class = BudgetManagerForm
    template_name = "budgets_manager/budget/budget.html"
    context_object_name = "budget"
    model = BudgetManager

    def form_valid(self, form):
        budget = form.save(commit=False)
        budget.save()
        return HttpResponseRedirect(
            reverse_lazy("home", kwargs={"user_id": self.request.user.pk})
        )
