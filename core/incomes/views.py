from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from incomes.forms import IncomeForm
from incomes.models import Income


class IncomesView(LoginRequiredMixin, FormView):
    template_name = "incomes/create_income.html"
    form_class = IncomeForm
    success_url = reverse_lazy("incomes:incomes-list")

    def get_success_url(self):
        return reverse_lazy("incomes:incomes-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "PATCH":
            income = get_object_or_404(
                Income, pk=self.kwargs["pk"], user=self.request.user
            )
            kwargs["instance"] = income
        return kwargs

    def form_valid(self, form):
        income = form.save(commit=False)
        income.user = self.request.user
        income.save()
        return super().form_valid(form)

    def delete(self, request, *args, **kwargs) -> HttpResponse:
        income_id: int = kwargs.get("income_pk")
        income_to_delete = get_object_or_404(Income, id=income_id, user=request.user)
        income_to_delete.delete()
        return JsonResponse({"message": "Income deleted successfully"}, status=200)


class GetIncomesView(LoginRequiredMixin, ListView):
    template_name: str = "incomes/incomes.html"
    model = Income
    context_object_name = "incomes"

    def get_queryset(self) -> QuerySet[Income]:
        return Income.objects.filter(user=self.request.user)
