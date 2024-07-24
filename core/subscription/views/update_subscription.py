from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import UpdateView
from subscription.forms import SubscriptionForm
from subscription.models import Subscription


class UpdateSubscriptionView(LoginRequiredMixin, UpdateView):
    model = Subscription
    template_name = "subscription/update-modal.html"
    success_url = reverse_lazy("home")
    context_object_name = "subscription"
    form_class = SubscriptionForm

    def get_context_data(self, **kwargs):
        kwargs["subscription_form"] = self.form_class()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.start_date = timezone.now()
        form.instance.end_date = timezone.now()
        form.instance.save()
        messages.success(
            self.request, f"Subscription updated successfully to {form.instance.plan}"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Subscription could not be updated")
        return super().form_valid(form)
