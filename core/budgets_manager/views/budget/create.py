from budgets_manager.forms.limit import BudgetManagerForm
from budgets_manager.models import BudgetManager
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView


class BudgetManagerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = BudgetManagerForm
    template_name = "budgets_manager/budget/budget-create.html"
    context_object_name = "budget"
    model = BudgetManager
    success_message = "Budget Manager has been created"

    def get_success_url(self):
        subscriptions = self.request.user.subscription_set
        if subscriptions.exists():
            last_subscription = subscriptions.last()
            if last_subscription.is_active:
                return reverse_lazy("home")
            else:
                return reverse_lazy(
                    "payment", kwargs={"payment_id": last_subscription.pk}
                )
        return reverse_lazy("subscription:list-create")

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        response = super().form_valid(form)
        form.instance.participants.add(self.request.user)
        return response

    def form_invalid(self, form) -> HttpResponse:
        messages.error(self.request, "Please try again.")
        return super().form_invalid(form)
