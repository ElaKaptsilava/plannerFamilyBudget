from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django_filters.views import FilterView

from expenses.filters import ExpenseFilter
from expenses.forms import ExpenseForm
from expenses.models import Expense, ExpenseCategory


class ExpenseView(LoginRequiredMixin, FilterView, FormView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expenses-list.html"
    context_object_name = "expenses"
    success_url = reverse_lazy("expenses:expenses-list")
    filterset_class = ExpenseFilter

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = ExpenseForm
        context["categories"] = ExpenseCategory.objects.filter(user=self.request.user)
        context["object_list"] = self.model.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form) -> HttpResponse:
        expense = form.save(commit=False)
        expense.user = self.request.user
        expense.save()
        messages.success(self.request, "The expense added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to add the expense. Please check the form."
        )
        return super().form_invalid(form)
