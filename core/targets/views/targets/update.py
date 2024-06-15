from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from targets.forms import TargetForm
from targets.models import Target


class TargetUpdateView(LoginRequiredMixin, UpdateView):
    model = Target
    form_class = TargetForm
    success_url = reverse_lazy("targets:targets-list")
    template_name = "targets/targets.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        self.object = form.save()
        messages.success(self.request, "The target updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form) -> HttpResponseRedirect:
        messages.error(self.request, "Failed to update target. Please check the form.")
        return super().form_invalid(form)
