from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django_filters.views import FilterView

from runningCosts.filters import RunningCostFilter
from runningCosts.forms import RunningCostForm
from runningCosts.models import RunningCost, RunningCostCategory


class RunningCostView(LoginRequiredMixin, FilterView, FormView):
    template_name = "runningCosts/running-costs-planner-list.html"
    form_class = RunningCostForm
    model = RunningCost
    context_object_name = "runningCost"
    success_url = reverse_lazy("running-costs:running-costs-list")
    filterset_class = RunningCostFilter

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["categories"] = RunningCostCategory.objects.all()
        context["object_list"] = self.model.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form) -> HttpResponseRedirect:
        running_cost = form.save(commit=False)
        running_cost.user = self.request.user
        running_cost.save()
        messages.success(self.request, "The running cost added successfully!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to add the running cost. Please check the form."
        )
        return HttpResponseRedirect(self.get_success_url())
