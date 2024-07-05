from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from runningCosts.forms import RunningCostCategoryForm
from runningCosts.models import RunningCostCategory


class CategoryCostUpdateView(UpdateView):
    model = RunningCostCategory
    form_class = RunningCostCategoryForm
    template_name = "runningCosts/category-list.html"
    success_url = reverse_lazy("running-costs:category-list")

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to update the category. Please check the form."
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "The category updated successfully!")
        return super().form_valid(form)
