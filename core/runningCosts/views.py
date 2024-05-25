from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django_filters.views import FilterView

from .filters import RunningCostFilter
from .models import RunningCost, RunningCostCategory


@method_decorator(login_required, name="dispatch")
class RunningCostListView(FilterView, ListView):
    model = RunningCost
    template_name = "runningCosts/running-costs-list.html"
    context_object_name = "runningCosts"
    filterset_class = RunningCostFilter

    def get_queryset(self) -> QuerySet[RunningCost]:
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = RunningCostCategory.objects.all()
        return context
