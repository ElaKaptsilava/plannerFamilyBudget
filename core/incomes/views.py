from accounts.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from incomes.forms import IncomeForm
from incomes.models import Income


class IncomesView(LoginRequiredMixin, View):
    template_name: str = "incomes/create_income.html"

    def post(self, request, *args, **kwargs) -> HttpResponse:
        context = dict()
        user: CustomUser = request.user
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            income_form.instance.user = request.user
            income_form.save()
            return redirect(reverse_lazy("home", kwargs={"user_id": user.pk}))
        context["income_form"] = income_form
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs) -> HttpResponse:
        form = IncomeForm()
        return render(request, self.template_name, {"income_form": form})

    def delete(self, request, *args, **kwargs) -> HttpResponse:
        income_id: int = kwargs.get("income_pk")
        income_to_delete = get_object_or_404(Income, id=income_id, user=request.user)
        income_to_delete.delete()
        return JsonResponse({"message": "Income deleted successfully"}, status=200)

    def patch(self, request, *args, **kwargs) -> HttpResponse:
        income_id = kwargs.get("income_pk")
        income = get_object_or_404(Income, pk=income_id, user=request.user)
        print(income)
        form = IncomeForm(request.POST, instance=income)
        print(form)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("home", kwargs={"user_id": request.user.pk}))
        return JsonResponse({"error": "Invalid data"}, status=400)


class GetIncomesView(LoginRequiredMixin, ListView):
    template_name: str = "incomes/incomes.html"
    model = Income
    context_object_name = "incomes"

    def get_queryset(self) -> QuerySet[Income]:
        return Income.objects.filter(user=self.request.user)
