from django.urls import reverse_lazy
from django.views.generic import UpdateView
from subscription.models import Subscription


class UpdateSubscriptionView(UpdateView):
    model = Subscription
    template_name = "subscription/update.html"
    success_url = reverse_lazy("home")
    context_object_name = "subscription"
