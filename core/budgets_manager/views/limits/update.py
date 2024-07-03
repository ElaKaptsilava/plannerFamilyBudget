from budgets_manager.forms import LimitForm
from budgets_manager.models import LimitManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView


class UpdateLimitView(LoginRequiredMixin, UpdateView):
    model = LimitManager
    form_class = LimitForm
    template_name = "budgets_manager/limits/list.html"
    success_url = reverse_lazy("manager:limits-list")
    context_object_name = "limit"
