from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from expenses.forms import ExpenseCategoryForm
from expenses.models import ExpenseCategory


class CategoryExpenseUpdateView(UpdateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = "expenses/category-list.html"
    success_url = reverse_lazy("expenses:category-list")

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to update the category. Please check the form."
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "The category updated successfully!")
        return super().form_valid(form)
