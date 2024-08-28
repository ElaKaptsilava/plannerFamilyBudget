import typing

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from subscription.forms import SubscriptionForm
from subscription.models import Status, Subscription


class CreateSubscriptionView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = "subscription/create_subscription.html"
    success_message = "Your subscription has been added!"

    def get_success_url(self):
        if self.object.payment.status != Status.COMPLETED:
            return reverse_lazy(
                "payment", kwargs={"payment_id": self.object.payment.pk}
            )
        return reverse_lazy("home")

    def get_context_data(self, **kwargs: typing.Any) -> dict:
        context = super().get_context_data(**kwargs)
        context["subscription_form"] = self.form_class
        return context

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        form.instance.save()
        return super().form_valid(form)

    def form_invalid(self, form) -> HttpResponse:
        messages.error(self.request, "Invalid form submission!")
        return super().form_invalid(form)
