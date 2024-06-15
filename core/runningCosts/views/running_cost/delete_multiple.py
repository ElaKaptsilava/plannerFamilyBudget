from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from runningCosts.models import RunningCost


class RunningCostDeleteMultipleView(LoginRequiredMixin, View):
    def post(self, request):
        selected_costs = request.POST.getlist("selected_costs")
        if selected_costs:
            RunningCost.objects.filter(pk__in=selected_costs).delete()
            messages.success(
                request, "Selected running costs were deleted successfully."
            )
        else:
            messages.error(request, "No running costs were selected.")
        return HttpResponseRedirect(reverse_lazy("running-costs:running-costs-list"))
