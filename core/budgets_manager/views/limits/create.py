from budgets_manager.forms.limit import LimitForm
from budgets_manager.models import LimitManager
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView


class LimitCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = LimitManager
    template_name = "budgets_manager/limits/list.html"
    context_object_name = "limit"
    form_class = LimitForm
    success_url = reverse_lazy("manager:limits-list")
    success_message = "The limit has been created."

    def form_valid(self, form) -> HttpResponse:
        form.instance.budget_manager = self.request.user.set_budget.budget
        return super().form_valid(form)

    def form_invalid(self, form):
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(f"{field.capitalize()}: {error}")

        error_message_str = (
            " | ".join(error_messages)
            if error_messages
            else "There was a problem with the form."
        )

        messages.error(
            self.request,
            f"Failed to add limit. Please check the form. {error_message_str}",
        )

        return super().form_invalid(form)
