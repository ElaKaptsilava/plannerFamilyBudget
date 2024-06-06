from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView

from .forms import TargetContributionForm, TargetForm
from .models import Target, TargetContribution


class TargetView(LoginRequiredMixin, FormView):
    model = Target
    template_name = "targets/targets.html"
    context_object_name = "targets"
    form_class = TargetForm
    success_url = reverse_lazy("targets:targets-list")

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["object_list"] = self.model.objects.filter(user=self.request.user)
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


class TargetUpdateView(LoginRequiredMixin, UpdateView):
    model = Target
    form_class = TargetForm
    success_url = reverse_lazy("targets:targets-list")
    template_name = "targets/targets.html"


class TargetDeleteMultipleView(LoginRequiredMixin, View):
    def post(self, request) -> HttpResponseRedirect:
        selected_targets = request.POST.getlist("selected_targets")
        if selected_targets:
            Target.objects.filter(pk__in=selected_targets).delete()
            messages.success(request, "Selected targets were deleted successfully.")
        else:
            messages.error(request, "No targets were selected.")
        return HttpResponseRedirect(reverse_lazy("targets:targets-list"))


class TargetContributionsView(LoginRequiredMixin, FormView):
    model = TargetContribution
    template_name = "targets/contributions.html"
    context_object_name = "targetContribution"
    form_class = TargetContributionForm

    def get_success_url(self) -> HttpResponseRedirect:
        target_pk = self.kwargs.get("pk")
        return reverse_lazy("targets:contributions-list", kwargs={"pk": target_pk})

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        queryset = self.get_queryset()
        context["object_list"] = queryset
        context["target"] = queryset.last().target
        return context

    def form_valid(self, form) -> HttpResponseRedirect:
        contribution = form.save(commit=False)
        contribution.user = self.request.user
        contribution.save()
        messages.success(self.request, "The contribution added successfully!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form) -> HttpResponseRedirect:
        messages.error(
            self.request, "Failed to add target contribution. Please check the form."
        )
        return super().form_invalid(form)

    def get_queryset(self):
        target_pk = self.kwargs.get("pk")

        return self.model.objects.filter(
            target__user=self.request.user, target__pk=target_pk
        )


class TargetContributionsDeleteMultipleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        target_pk = kwargs.get("pk")
        selected_contributions = request.POST.getlist("selected_contributions")
        if target_pk:
            TargetContribution.objects.filter(
                target__pk=target_pk, pk__in=selected_contributions
            ).delete()
            messages.success(request, "Target Contributions were deleted successfully.")
        else:
            messages.error(request, "No target contributions were selected.")
        return HttpResponseRedirect(
            reverse_lazy("targets:contributions-list", kwargs={"pk": target_pk})
        )
