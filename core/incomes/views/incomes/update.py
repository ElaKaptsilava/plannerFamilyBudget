from accounts.mixins.ownership import OwnerRequiredMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from incomes.forms import IncomeForm
from incomes.models import Income


class IncomeUpdateView(
    LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView
):
    form_class = IncomeForm
    model = Income
    success_url = reverse_lazy("incomes:incomes-list")
    context_object_name = "incomes"
    template_name: str = "incomes/list.html"
    success_message = "Income updated successfully"

    def get_queryset(self) -> QuerySet[Income]:
        return self.request.user.set_budget.budget.get_annual_incomes()

    def form_invalid(self, form) -> HttpResponseRedirect:
        messages.error(
            self.request, "Failed to update the income. Please check the form."
        )
        return HttpResponseRedirect(self.success_url)

    def form_valid(self, form) -> HttpResponseRedirect:
        """If the form is valid, save the associated model."""
        messages.success(self.request, "The income updated successfully!")
        return super().form_valid(form)
