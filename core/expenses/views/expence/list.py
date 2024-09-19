from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django_filters.views import FilterView
from expenses.filters import ExpenseFilter
from expenses.forms import ExpenseForm
from expenses.models import Expense, ExpenseCategory


class ExpensesListView(LoginRequiredMixin, FilterView, ListView):
    model = Expense
    template_name = "expenses/expenses-list.html"
    context_object_name = "expenses"
    success_url = reverse_lazy("expenses:expenses-list")
    filterset_class = ExpenseFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.filter(budget=self.request.user.set_budget.budget)

    def get_context_data(self, **kwargs) -> dict:
        context = {
            "form": ExpenseForm(),
            "categories": ExpenseCategory.objects.filter(user=self.request.user),
        }
        kwargs.update(context)
        if not self.object_list:
            messages.info(
                self.request, "You haven't added any expenses yet. Start by adding one!"
            )
        return super().get_context_data(**kwargs)
