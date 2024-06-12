from budgets_manager.forms import BudgetManagerForm
from budgets_manager.models import BudgetManager
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


class BudgetManagerFormView(CreateView):
    form_class = BudgetManagerForm
    template_name = "budgets_manager/budget/budget-create.html"
    context_object_name = "budget"
    model = BudgetManager

    # def get_success_url(self):
    #     return reverse_lazy("home", {"user_id": self.request.user.pk})

    def form_valid(self, form) -> HttpResponse:
        budget = form.save(commit=False)
        budget.user = self.request.user
        budget.save()
        print("Budget: ", budget)
        return HttpResponseRedirect(
            reverse_lazy("home", kwargs={"user_id": self.request.user.pk})
        )
