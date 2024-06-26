from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView
from runningCosts.models import RunningCostCategory


class CategoryListView(LoginRequiredMixin, ListView):
    model = RunningCostCategory
    template_name = "runningCosts/category-list.html"

    def get_queryset(self) -> QuerySet[RunningCostCategory]:
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.get_queryset()
        return context
