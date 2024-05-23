from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView
from incomes.forms import IncomeForm
from incomes.models import Income


class IncomesView(LoginRequiredMixin, FormView):
    template_name = "incomes/create_income.html"
    form_class = IncomeForm
    success_url = reverse_lazy("incomes:incomes-list")

    def get_object(self):
        if "pk" in self.kwargs:
            return get_object_or_404(Income, pk=self.kwargs["pk"])
        return None

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        if self.request.method in ["POST", "PATCH"] and self.get_object():
            kwargs["instance"] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["incomes"] = Income.objects.filter(user=self.request.user)
        context["form"] = self.get_form()
        return context

    def form_valid(self, form) -> HttpResponse:
        income = form.save(commit=False)
        income.user = self.request.user
        income.save()
        return super().form_valid(form)

    def delete(self, request, *args, **kwargs) -> HttpResponse:
        income_id: int = kwargs.get("income_pk")
        income_to_delete = get_object_or_404(Income, id=income_id, user=request.user)
        income_to_delete.delete()
        return self.success_url


class GetIncomesView(LoginRequiredMixin, ListView):
    template_name: str = "incomes/incomes.html"
    model = Income
    context_object_name = "incomes"

    def get_queryset(self) -> QuerySet[Income]:
        return Income.objects.filter(user=self.request.user)


class DeleteMultipleIncomesView(View):
    def post(self, request):
        selected_incomes = request.POST.getlist("selected_incomes")
        if selected_incomes:
            Income.objects.filter(id__in=selected_incomes).delete()
            messages.success(request, "Selected incomes were deleted successfully.")
        else:
            messages.error(request, "No incomes were selected.")
        return redirect(reverse("incomes:incomes-list"))
