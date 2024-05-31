from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import TargetForm
from .models import Target


class TargetListView(LoginRequiredMixin, FormView):
    model = Target
    template_name = "targets/targets.html"
    context_object_name = "targets"
    form_class = TargetForm
    success_url = reverse_lazy("targets:targets-list")

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

    def form_valid(self, form) -> HttpResponseRedirect:
        target = form.save(commit=False)
        target.user = self.request.user
        target.save()
        return HttpResponseRedirect(self.get_success_url())
