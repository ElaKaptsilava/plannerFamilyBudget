from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from targets.forms import (
    SavingNegativeContributionsForm,
    SavingPositiveContributionsForm,
)
from targets.models import SavingContributions


class PositiveCreateView(LoginRequiredMixin, CreateView):
    model = SavingContributions
    form_class = SavingPositiveContributionsForm
    template_name = "index.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form) -> HttpResponseRedirect:
        form.instance.saving = self.request.user.saving
        return super().form_valid(form)


class NegativeCreateView(LoginRequiredMixin, CreateView):
    model = SavingContributions
    form_class = SavingNegativeContributionsForm
    template_name = "index.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form) -> HttpResponseRedirect:
        form.instance.saving = self.request.user.saving
        return super().form_valid(form)
