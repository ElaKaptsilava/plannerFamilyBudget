from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from expenses.forms import ExpenseCategoryForm
from expenses.models import ExpenseCategory


class CategoryCreateView(LoginRequiredMixin, CreateView):
    form_class = ExpenseCategoryForm
    model = ExpenseCategory
    template_name = "expenses/expenses-create-modal.html"
    success_url = reverse_lazy("expenses:expenses-list")

    def form_valid(self, form) -> HttpResponse:
        category = form.save(commit=False)
        category.user = self.request.user
        category.save()
        messages.success(self.request, "The category was added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to add the category. Please check the form."
        )
        return super().form_invalid(form)
