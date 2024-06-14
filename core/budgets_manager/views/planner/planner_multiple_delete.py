from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View

from budgets_manager.models import PlannerManager


class PlannerMultipleDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        planners_selected = request.POST.getlist("planners_selected")
        if planners_selected:
            PlannerManager.objects.filter(id__in=planners_selected).delete()
            messages.success(request, "Selected planners was successfully deleted")
        else:
            messages.error(request, "No planners selected")
        return HttpResponseRedirect(reverse_lazy("manager:planner-list", kwargs=kwargs))
