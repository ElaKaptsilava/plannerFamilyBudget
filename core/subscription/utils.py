from django.http import HttpResponse
from django.urls import reverse_lazy


def check_is_user_has_subscription(request) -> HttpResponse | None:
    subscription_url = reverse_lazy("subscription:list-create")
    if not hasattr(request.user, "subscription") and request.path != subscription_url:
        return subscription_url
