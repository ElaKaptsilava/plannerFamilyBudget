from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django_filters.views import FilterView
from incomes.filters import IncomeFilter
from incomes.forms import IncomeForm
from incomes.models import Income
from multi_user.models import FamilyBudget


class IncomesView(LoginRequiredMixin, FilterView, FormView):
    template_name: str = "incomes/list.html"
    model = Income
    context_object_name = "incomes"
    filterset_class = IncomeFilter
    form_class = IncomeForm
    success_url = reverse_lazy("incomes:incomes-list")

    def get_members_queryset(self) -> QuerySet[FamilyBudget]:
        return FamilyBudget.objects.get(owner=self.request.user).members.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.filter(user__in=self.get_members_queryset())

    def form_valid(self, form) -> HttpResponseRedirect:
        income = form.save(commit=False)
        income.user = self.request.user
        income.save()
        messages.success(self.request, "The income added successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["object_list"] = self.get_queryset()
        context["custom_message"] = (
            "You haven't added any incomes yet. Start by adding one!"
        )
        if not self.get_queryset():
            messages.info(self.request, "You haven't added any incomes yet.")
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Failed to add income. Please check the form.")
        return super().form_invalid(form)
