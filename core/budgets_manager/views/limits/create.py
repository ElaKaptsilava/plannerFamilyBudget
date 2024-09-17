from budgets_manager.forms.limit import LimitForm
from budgets_manager.models import LimitManager
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView


class LimitCreateView(LoginRequiredMixin, CreateView):
    model = LimitManager
    template_name = "budgets_manager/limits/list.html"
    context_object_name = "limit"
    form_class = LimitForm
    success_url = reverse_lazy("manager:limits-list")

    def form_valid(self, form) -> HttpResponse:
        form.instance.budget_manager = self.request.user.budgetmanager
        messages.success(self.request, "The plan added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to add plan. Please check the form.")
        return super().form_invalid(form)
