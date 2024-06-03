from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView

from .forms import TargetForm
from .models import Target


class TargetView(LoginRequiredMixin, FormView):
    model = Target
    template_name = "targets/targets.html"
    context_object_name = "targets"
    form_class = TargetForm
    success_url = reverse_lazy("targets:targets-list")

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["object_list"] = Target.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form) -> HttpResponseRedirect:
        target = form.save(commit=False)
        target.user = self.request.user
        target.save()
        return HttpResponseRedirect(self.get_success_url())


class TargetUpdateView(LoginRequiredMixin, UpdateView):
    model = Target
    form_class = TargetForm
    success_url = reverse_lazy("targets:targets-list")
    template_name = "targets/targets.html"


class TargetDeleteMultipleView(LoginRequiredMixin, View):
    def post(self, request):
        print(request.POST)
        selected_targets = request.POST.getlist("selected_targets")
        print(selected_targets)
        if selected_targets:
            Target.objects.filter(pk__in=selected_targets).delete()
            messages.success(request, "Selected targets were deleted successfully.")
        else:
            messages.error(request, "No targets were selected.")
        return HttpResponseRedirect(reverse_lazy("targets:targets-list"))
