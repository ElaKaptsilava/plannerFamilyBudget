from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from expenses.forms import ExpenseForm
from expenses.models import Expense


class ExpensesCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expenses-list.html"
    context_object_name = "expenses"
    success_url = reverse_lazy("expenses:expenses-list")

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        messages.success(self.request, "The expense added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form) -> HttpResponse:
        messages.error(
            self.request, "Failed to add the expense. Please check the form."
        )
        return super().form_invalid(form)
