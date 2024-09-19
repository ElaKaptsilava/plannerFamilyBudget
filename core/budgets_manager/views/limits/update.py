from accounts.mixins.ownership import OwnerRequiredMixin
from budgets_manager.forms.limit import LimitForm
from budgets_manager.models import LimitManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView


class UpdateLimitView(
    LoginRequiredMixin, SuccessMessageMixin, OwnerRequiredMixin, UpdateView
):
    model = LimitManager
    form_class = LimitForm
    template_name = "budgets_manager/limits/update-modal.html"
    success_url = reverse_lazy("manager:limits-list")
    context_object_name = "limit"
    success_message = "Limit updated successfully!"
