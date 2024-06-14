from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from expenses.forms import ExpenseForm
from expenses.models import Expense


class ExpensesUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ExpenseForm
    model = Expense
    template_name = "expenses/expenses-list.html"
    context_object_name = "expenses"
    success_url = reverse_lazy("expenses:expenses-list")

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to update the expense. Please check the form."
        )
        return HttpResponseRedirect(self.success_url)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        response = super().form_valid(form)
        messages.success(self.request, "The expense updated successfully!")
        return response
