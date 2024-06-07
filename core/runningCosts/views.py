from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView
from django_filters.views import FilterView

from .filters import RunningCostFilter
from .forms import RunningCostForm
from .models import RunningCost, RunningCostCategory


class RunningCostView(LoginRequiredMixin, FilterView, FormView):
    template_name = "runningCosts/running-costs-list.html"
    form_class = RunningCostForm
    model = RunningCost
    context_object_name = "runningCost"
    success_url = reverse_lazy("running-costs:running-costs-list")
    filterset_class = RunningCostFilter

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["categories"] = RunningCostCategory.objects.all()
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


class RunningCostDeleteMultipleView(LoginRequiredMixin, View):
    def post(self, request):
        selected_costs = request.POST.getlist("selected_costs")
        if selected_costs:
            RunningCost.objects.filter(pk__in=selected_costs).delete()
            messages.success(
                request, "Selected running costs were deleted successfully."
            )
        else:
            messages.error(request, "No running costs were selected.")
        return HttpResponseRedirect(reverse_lazy("running-costs:running-costs-list"))


class RunningCostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RunningCostForm
    model = RunningCost
    success_url = reverse_lazy("running-costs:running-costs-list")
    context_object_name = "runningCost"
    template_name = "runningCosts/running-costs-list.html"

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to update the running cost. Please check the form."
        )
        return HttpResponseRedirect(self.success_url)

    @transaction.atomic
    def form_valid(self, form):
        self.object = form.save()
        response = super().form_valid(form)
        messages.success(self.request, "The running cost updated successfully!")
        return response
