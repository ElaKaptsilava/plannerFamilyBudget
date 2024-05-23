from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView

from .models import Expense


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    context_object_name = "expenses"
    template_name = "expenses/expenses-list.html"

    def get_queryset(self) -> QuerySet[Expense]:
        return self.model.objects.filter(user=self.request.user)
