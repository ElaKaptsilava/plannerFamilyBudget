from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from subscription.forms.subscription import SubscriptionForm
from subscription.models.subscription import Subscription


class CreateSubscriptionView(LoginRequiredMixin, CreateView):
    model = Subscription
    form_class = SubscriptionForm
    success_url = reverse_lazy("home")
    template_name = "subscription/create_subscription.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscription_form"] = self.form_class
        return context

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        form.instance.end_date = timezone.now() + timedelta(
            days=30
        )  # pip install python-dateutil
        form.instance.save()
        messages.success(self.request, "Your subscription has been added!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form submission!")
        return super().form_invalid(form)
