from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from targets.forms import TargetForm
from targets.models import Target


class TargetsView(LoginRequiredMixin, FormView):
    model = Target
    template_name = "targets/targets.html"
    context_object_name = "targets"
    form_class = TargetForm
    success_url = reverse_lazy("targets:targets-list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).prefetch_related(
            "user", "targetcontribution_set"
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["object_list"] = self.get_queryset()
        context["custom_message"] = (
            "You haven't added any contributions yet. Start by adding one!"
        )
        if not self.get_queryset():
            messages.info(self.request, "You haven't added any contributions yet.")
        return context

    def form_valid(self, form) -> HttpResponseRedirect:
        target = form.save(commit=False)
        target.user = self.request.user
        target.save()
        messages.success(self.request, "The target added successfully!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form) -> HttpResponseRedirect:
        messages.error(self.request, "Failed to add target. Please check the form.")
        return super().form_invalid(form)
