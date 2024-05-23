from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView

from .forms import ExpenseCategoryForm, ExpenseForm
from .models import Expense, ExpenseCategory


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = "expenses/expenses-list.html"
    context_object_name = "expenses"

    def get_queryset(self) -> QuerySet[Expense]:
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ExpenseCategory.objects.all()
        return context


class ExpenseView(LoginRequiredMixin, FormView):
    model = Expense
    form_class = ExpenseForm
    context_object_name = "expenses"
    template_name = "expenses/expenses-list.html"
    success_url = reverse_lazy("expenses:expenses-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ExpenseCategory.objects.all()
        context["form"] = self.get_form()
        print(context["form"])

        return context

    def form_valid(self, form) -> HttpResponse:
        expense = form.save(commit=False)
        expense.user = self.request.user
        expense.save()
        return super().form_valid(form)


class ExpenseCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = "expenses/expenses-list.html"
    success_url = reverse_lazy("expenses:expenses-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.model.objects.all()
        context["form"] = self.get_form()
        return context
