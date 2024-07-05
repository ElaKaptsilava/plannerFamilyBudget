from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from runningCosts.models import RunningCostCategory


class CategoryCostDeleteView(LoginRequiredMixin, DeleteView):
    model = RunningCostCategory
    template_name = "runningCosts/category-list.html"
    success_url = reverse_lazy("running-costs:category-list")
