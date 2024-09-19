from accounts.mixins.ownership import OwnerRequiredMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from expenses.forms import ExpenseForm
from expenses.models import Expense


class ExpensesUpdateView(
    LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView
):
    form_class = ExpenseForm
    model = Expense
    template_name = "expenses/expenses-list.html"
    context_object_name = "expenses"
    success_url = reverse_lazy("expenses:expenses-list")
    success_message = "Updated expenses."

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to update the expense. Please check the form."
        )
        return HttpResponseRedirect(self.success_url)
