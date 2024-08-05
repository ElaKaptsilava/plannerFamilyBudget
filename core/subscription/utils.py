from django.urls import reverse_lazy
from django.utils import timezone


def check_is_user_has_subscription(request) -> str | None:
    subscription_url = reverse_lazy("subscription:list-create")
    today = timezone.now().date()
    subscription_exist = request.user.subscription_set.filter(
        end_date__gte=today, start_date__lte=today
    ).exists()
    if request.path != subscription_url and not subscription_exist:
        return subscription_url
