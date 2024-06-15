from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from runningCosts.forms import RunningCostForm
from runningCosts.models import RunningCost


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
        return super().form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        response = super().form_valid(form)
        messages.success(self.request, "The running cost updated successfully!")
        return response
