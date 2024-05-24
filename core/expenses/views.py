from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, ListView

from .forms import ExpenseCategoryForm, ExpenseFilterForm, ExpenseForm
from .models import Expense, ExpenseCategory


@method_decorator(login_required, name="dispatch")
class ExpenseListView(ListView):
    model = Expense
    template_name = "expenses/expenses-list.html"
    context_object_name = "expenses"

    def get_queryset(self) -> QuerySet[Expense]:
        queryset = super().get_queryset().filter(user=self.request.user)
        print("Request GET data:", self.request.GET)
        form = ExpenseFilterForm(self.request.GET)
        if form.is_valid():
            print("Form cleaned data:", form.cleaned_data)
            if form.cleaned_data["category"]:
                queryset = queryset.filter(category=form.cleaned_data["category"])
                print(queryset)
            if form.cleaned_data["min_amount"]:
                queryset = queryset.filter(amount__gte=form.cleaned_data["min_amount"])
            if form.cleaned_data["max_amount"]:
                queryset = queryset.filter(amount__lte=form.cleaned_data["max_amount"])
            if form.cleaned_data["start_date"]:
                queryset = queryset.filter(
                    datetime__gte=form.cleaned_data["start_date"]
                )
            if form.cleaned_data["end_date"]:
                queryset = queryset.filter(datetime__lte=form.cleaned_data["end_date"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ExpenseFilterForm(self.request.GET)
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
