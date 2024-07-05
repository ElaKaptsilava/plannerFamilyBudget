from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView
from runningCosts.forms import RunningCostCategoryForm
from runningCosts.models import RunningCostCategory


class CategoryListView(LoginRequiredMixin, ListView):
    model = RunningCostCategory
    template_name = "runningCosts/category-list.html"

    def get_queryset(self) -> QuerySet[RunningCostCategory]:
        return self.model.objects.prefetch_related("running_costs").filter(
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.get_queryset()
        context["form_category"] = RunningCostCategoryForm()
        context["category_update"] = {
            category.pk: RunningCostCategoryForm(instance=category)
            for category in self.object_list
        }.items()
        if not self.get_queryset():
            messages.info(self.request, "You haven't added any costs yet.")
        return context
