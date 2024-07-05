from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from expenses.models import ExpenseCategory


class CategoryExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = ExpenseCategory
    template_name = "expenses/category-list.html"
    success_url = reverse_lazy("expenses:category-list")

    def get_success_url(self):
        messages.warning(self.request, "Category expense deleted successfully.")
        return super().get_success_url()
