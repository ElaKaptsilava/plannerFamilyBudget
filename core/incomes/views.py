from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from incomes.forms import IncomeForm


class IncomesView(View, LoginRequiredMixin):
    template_name = "incomes/create_income.html"

    def post(self, request, *args, **kwargs):
        context = {}
        user = request.user
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            income_form.save()
            return redirect(reverse_lazy("home", kwargs={"user_id": user.id}))
        context["form"] = income_form
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        income_form = IncomeForm()
        context = {"form": income_form}
        return render(request, self.template_name, context)
