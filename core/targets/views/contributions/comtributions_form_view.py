from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from targets.forms import TargetContributionForm
from targets.models import Target, TargetContribution


class TargetContributionsView(LoginRequiredMixin, FormView):
    model = TargetContribution
    template_name = "targets/contributions.html"
    context_object_name = "targetContribution"
    form_class = TargetContributionForm

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_success_url(self) -> HttpResponseRedirect:
        target_pk = self.kwargs.get("pk")
        return reverse_lazy("targets:contributions-list", kwargs={"pk": target_pk})

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["object_list"] = self.get_queryset()
        context["target_pk"] = self.kwargs["pk"]
        context["custom_message"] = (
            "You haven't added any contributions yet. Start by adding one!"
        )
        return context

    def form_valid(self, form) -> HttpResponseRedirect:
        target_pk = self.kwargs.get("pk")
        target = Target.objects.get(pk=target_pk)
        contribution = form.save(commit=False)
        contribution.user = self.request.user
        contribution.target = target
        contribution.save()
        messages.success(self.request, "The contribution added successfully!")
        return HttpResponseRedirect(self.get_success_url())
