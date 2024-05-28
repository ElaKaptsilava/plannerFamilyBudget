from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView
from django_filters.views import FilterView
from incomes.filters import IncomeFilter
from incomes.forms import IncomeForm
from incomes.models import Income


class IncomesView(LoginRequiredMixin, FilterView, FormView):
    template_name: str = "incomes/incomes.html"
    model = Income
    context_object_name = "incomes"
    filterset_class = IncomeFilter
    form_class = IncomeForm

    def form_valid(self, form) -> HttpResponseRedirect:
        income = form.save(commit=False)
        income.user = self.request.user
        income.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context


class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    form_class = IncomeForm
    model = Income
    success_url = reverse_lazy("incomes:incomes-list")
    context_object_name = "incomes"
    template_name: str = "incomes/incomes.html"


class DeleteMultipleIncomesView(LoginRequiredMixin, View):
    def post(self, request):
        selected_incomes = request.POST.getlist("selected_incomes")
        if selected_incomes:
            Income.objects.filter(id__in=selected_incomes).delete()
            messages.success(request, "Selected incomes were deleted successfully.")
        else:
            messages.error(request, "No incomes were selected.")
        return redirect(reverse("incomes:incomes-list"))
