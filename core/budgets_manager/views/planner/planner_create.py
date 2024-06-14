from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from budgets_manager.models import PlannerManager
from budgets_manager.forms import PlannerForm


class PlannerCreateView(LoginRequiredMixin, CreateView):
    model = PlannerManager
    template_name = "budgets_manager/planner/planner-list.html"
    context_object_name = "planner"
    form_class = PlannerForm
    success_url = reverse_lazy("manager:planner-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        return context

    def form_valid(self, form):
        plan = form.save(commit=False)
        plan.user = self.request.user
        plan.budget_manager = self.request.user.budgetmanager
        plan.save()
        messages.success(self.request, "The plan added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to add plan. Please check the form.")
        return super().form_invalid(form)
