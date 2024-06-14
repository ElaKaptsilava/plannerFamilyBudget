from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from targets.models import TargetContribution


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
