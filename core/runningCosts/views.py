from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView
from django_filters.views import FilterView

from .filters import RunningCostFilter
from .forms import RunningCostForm
from .models import RunningCost


class RunningCostView(LoginRequiredMixin, FilterView, FormView):  # ListView
    template_name = "runningCosts/running-costs-list.html"
    form_class = RunningCostForm
    model = RunningCost
    context_object_name = "runningCost"
    success_url = reverse_lazy("running-costs:running-costs-list")
    filterset_class = RunningCostFilter

    def get_object(self):
        if "pk" in self.kwargs:
            return get_object_or_404(RunningCost, pk=self.kwargs["pk"])
        return None

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        if self.request.method in ["POST", "PATCH"] and self.get_object():
            kwargs["instance"] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["runningCosts"] = RunningCost.objects.filter(user=self.request.user)
        context["form"] = self.get_form()
        return context

    def form_valid(self, form) -> HttpResponse:
        running_cost = form.save(commit=False)
        running_cost.user = self.request.user
        running_cost.save()
        return super().form_valid(form)
