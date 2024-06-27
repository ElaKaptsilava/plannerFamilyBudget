from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView
from expenses.forms import ExpenseCategoryForm
from expenses.models import ExpenseCategory


class CategoryListView(LoginRequiredMixin, ListView):
    model = ExpenseCategory
    template_name = "expenses/category-list.html"

    def get_queryset(self) -> QuerySet[ExpenseCategory]:
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.get_queryset()
        context["form_category"] = ExpenseCategoryForm()
        if not self.get_queryset():
            messages.info(self.request, "No expenses found.")
        return context
