from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View

from targets.models import Target


class TargetDeleteMultipleView(LoginRequiredMixin, View):
    def post(self, request) -> HttpResponseRedirect:
        selected_targets = request.POST.getlist("selected_targets")
        if selected_targets:
            Target.objects.filter(pk__in=selected_targets).delete()
            messages.success(request, "Selected targets were deleted successfully.")
        else:
            messages.error(request, "No targets were selected.")
        return HttpResponseRedirect(reverse_lazy("targets:targets-list"))
