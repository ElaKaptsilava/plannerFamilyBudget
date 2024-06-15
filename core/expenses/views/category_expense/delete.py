from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View
from expenses.models import ExpenseCategory


class CategoryExpenseDeleteView(LoginRequiredMixin, View):
    model = ExpenseCategory
    template_name = "expenses/category-list.html"
    success_url = reverse_lazy("expenses:category-list")

    def post(self, request, *args, **kwargs):
        category_pk = self.kwargs.get("pk")
        if category_pk:
            self.model.objects.get(pk=category_pk).delete()
            messages.success(request, "Category deleted successfully.")
        return HttpResponseRedirect(reverse_lazy("expenses:expenses-list"))
