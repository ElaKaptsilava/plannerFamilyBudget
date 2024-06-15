from budgets_manager.models import LimitManager
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View


class PlannerMultipleDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        selected = request.POST.getlist("selected")
        if selected:
            LimitManager.objects.filter(id__in=selected).delete()
            messages.success(request, "Selected planners was successfully deleted")
        else:
            messages.error(request, "No planners selected")
        return HttpResponseRedirect(reverse_lazy("manager:limits-list", kwargs=kwargs))
