from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django_filters.views import FilterView
from expenses.filters import ExpenseFilter
from expenses.forms import ExpenseForm
from expenses.models import Expense, ExpenseCategory


class ExpensesView(LoginRequiredMixin, FilterView, FormView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expenses-list.html"
    context_object_name = "expenses"
    success_url = reverse_lazy("expenses:expenses-list")
    filterset_class = ExpenseFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        context["categories"] = ExpenseCategory.objects.filter(user=self.request.user)
        context["object_list"] = self.get_queryset()
        context["custom_message"] = (
            "You haven't added any costs yet. Start by adding one!"
        )
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
