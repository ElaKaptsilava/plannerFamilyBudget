from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from subscription.forms.subscription import SubscriptionForm
from subscription.models import Plan
from subscription.models.subscription import Subscription


class CreateSubscriptionView(LoginRequiredMixin, CreateView):
    model = Subscription
    form_class = SubscriptionForm
    success_url = reverse_lazy("home")
    template_name = "subscription/create_subscription.html"

    def get_context_data(self, **kwargs):
        kwargs["subscription_form"] = self.form_class
        kwargs["plans"] = Plan.objects.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        form.instance.save()
        messages.success(self.request, "Your subscription has been added!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form submission!")
        return super().form_invalid(form)
