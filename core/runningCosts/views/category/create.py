from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from runningCosts.forms import RunningCostCategoryForm
from runningCosts.models import RunningCostCategory


class CategoryCreateView(LoginRequiredMixin, CreateView):
    form_class = RunningCostCategoryForm
    model = RunningCostCategory
    template_name = "runningCosts/category-create-modal.html"
    success_url = reverse_lazy("running-costs:category-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_category"] = RunningCostCategoryForm()
        return context

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        messages.success(self.request, "The category was added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to add the category. Please check the form."
        )
        return super().form_invalid(form)
