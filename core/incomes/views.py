from accounts.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from incomes.forms import IncomeForm
from incomes.models import Income


class IncomesView(View, LoginRequiredMixin):
    template_name: str = "incomes/create_income.html"
    login_url: reverse_lazy = reverse_lazy("accounts:login")

    def post(self, request, *args, **kwargs) -> HttpResponse:
        context = dict()
        user: CustomUser = request.user
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            if isinstance(request.user, CustomUser):
                income_form.instance.user = request.user
                income_form.save()
                return redirect(reverse_lazy("home", kwargs={"user_id": user.pk}))
            else:
                raise TypeError(
                    "The 'id' field expected a number but got an invalid user object."
                )
        context["income_form"] = income_form
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            form = IncomeForm()
            return render(request, self.template_name, {"income_form": form})
        return redirect(self.login_url)

    def delete(self, request, *args, **kwargs) -> HttpResponse:
        print(kwargs)
        if request.user.is_authenticated:
            income_id = kwargs.get("income_pk")
            income_to_delete = get_object_or_404(
                Income, id=income_id, user=request.user
            )
            income_to_delete.delete()
            return JsonResponse({"message": "Income deleted successfully"}, status=200)
        return redirect(self.login_url)


class GetIncomesView(View, LoginRequiredMixin):
    template_name: str = "incomes/incomes.html"
    login_url: reverse_lazy = reverse_lazy("accounts:login")
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            incomes = Income.objects.filter(user=request.user)
            return render(request, self.template_name, {"incomes": incomes})
        return redirect(self.login_url)
