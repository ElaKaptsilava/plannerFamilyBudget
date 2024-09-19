from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django_filters.views import FilterView
from incomes.filters import IncomeFilter
from incomes.forms import IncomeForm
from incomes.models import Income


class IncomesView(LoginRequiredMixin, FilterView, FormView):
    template_name: str = "incomes/list.html"
    model = Income
    context_object_name = "incomes"
    filterset_class = IncomeFilter
    form_class = IncomeForm
    success_url = reverse_lazy("incomes:incomes-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.filter(
            user__in=self.request.user.set_budget.budget.participants.all()
        )

    def form_valid(self, form) -> HttpResponseRedirect:
        form.instance.user = self.request.user
        form.instance.budget = self.request.user
        messages.success(self.request, "The income added successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        context = {
            "form": self.get_form(),
        }
        kwargs.update(context)
        if not self.get_queryset():
            messages.info(self.request, "You haven't added any incomes yet.")
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to add income. Please check the form.")
        return super().form_invalid(form)
