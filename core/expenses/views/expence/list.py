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
        return self.filterset.qs.filter(user=self.request.user).select_related(
            "category"
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = ExpenseForm()
        context["categories"] = ExpenseCategory.objects.filter(user=self.request.user)
        context["object_list"] = self.get_queryset()
        if not context["object_list"]:
            messages.info(
                self.request, "You haven't added any expenses yet. Start by adding one!"
            )
        return context
