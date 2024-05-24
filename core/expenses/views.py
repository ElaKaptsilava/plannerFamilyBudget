from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, FormView, ListView
from django_filters.views import FilterView

from .filters import ExpenseFilter
from .forms import ExpenseCategoryForm, ExpenseForm
from .models import Expense, ExpenseCategory


@method_decorator(login_required, name="dispatch")
class ExpenseListView(FilterView, ListView):
    model = Expense
    template_name = "expenses/expenses-list.html"
    context_object_name = "expenses"
    filterset_class = ExpenseFilter

    def get_queryset(self) -> QuerySet[Expense]:
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset

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

    def get_object(self, *args, **kwargs):
        if "pk" in self.kwargs:
            return get_object_or_404(Expense, pk=self.kwargs["pk"])
        return None

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        if self.request.method in ["POST", "PATCH"] and self.get_object():
            kwargs["instance"] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ExpenseCategory.objects.all()
        context["expenses"] = Expense.objects.filter(user=self.request.user)
        context["form"] = self.get_form()
        return context

    def form_valid(self, form) -> HttpResponse:
        expense = form.save(commit=False)
        expense.user = self.request.user
        expense.save()
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class DeleteMultipleExpenseView(View):
    def post(self, request):
        selected_incomes = request.POST.getlist("selected_incomes")
        if selected_incomes:
            Expense.objects.filter(id__in=selected_incomes).delete()
            messages.success(request, "Selected incomes were deleted successfully.")
        else:
            messages.error(request, "No incomes were selected.")
        return HttpResponseRedirect(reverse_lazy("expenses:expenses-list"))


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
