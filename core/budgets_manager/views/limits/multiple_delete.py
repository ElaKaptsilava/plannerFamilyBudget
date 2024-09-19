from budgets_manager.models import LimitManager
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View


class LimitMultipleDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        selected = request.POST.getlist("selected")
        if selected:
            limits_to_delete = LimitManager.objects.filter(id__in=selected)
            deleted_names = limits_to_delete.values_list("name", flat=True)

            limits_to_delete.delete()

            if deleted_names:
                deleted_names_list = ", ".join(deleted_names)
                messages.success(
                    self.request,
                    f"Selected planners were successfully deleted: {deleted_names_list}",
                )
            else:
                messages.success(
                    self.request, "Selected planners were successfully deleted"
                )
        else:
            messages.error(self.request, "No planners selected")
        return HttpResponseRedirect(reverse_lazy("manager:limits-list", kwargs=kwargs))
