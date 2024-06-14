from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView

from budgets_manager.forms import PlannerForm
from budgets_manager.models import PlannerManager


class PlannerListView(LoginRequiredMixin, ListView):
    model = PlannerManager
    template_name = "budgets_manager/planner/planner-list.html"
    context_object_name = "planner"

    def get_queryset(self) -> QuerySet[PlannerManager]:
        return PlannerManager.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        context["form"] = PlannerForm()
        return context
