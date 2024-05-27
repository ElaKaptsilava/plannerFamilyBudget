from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, UpdateView
from django_filters.views import FilterView

from .filters import ExpenseFilter
from .forms import ExpenseForm
from .models import Expense, ExpenseCategory


class ExpenseView(LoginRequiredMixin, FilterView, FormView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expenses-list.html"
    context_object_name = "expenses"
    success_url = reverse_lazy("expenses:expenses-list")
    filterset_class = ExpenseFilter

    def form_valid(self, form) -> HttpResponse:
        expense = form.save(commit=False)
        expense.user = self.request.user
        expense.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        if "form" not in kwargs:
            kwargs["form"] = ExpenseForm
        kwargs["categories"] = ExpenseCategory.objects.all()
        kwargs["expenses"] = Expense.objects.filter(user=self.request.user)
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name="dispatch")
class DeleteMultipleExpenseView(View):
    def post(self, request):
        selected_expenses = request.POST.getlist("selected_expenses")
        if selected_expenses:
            Expense.objects.filter(id__in=selected_expenses).delete()
            messages.success(request, "Selected expenses were deleted successfully.")
        else:
            messages.error(request, "No expenses were selected.")
        return HttpResponseRedirect(reverse_lazy("expenses:expenses-list"))


class ExpensesUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ExpenseForm
    model = Expense
    template_name = "expenses/expenses-list.html"
    context_object_name = "expenses"
    success_url = reverse_lazy("expenses:expenses-list")
