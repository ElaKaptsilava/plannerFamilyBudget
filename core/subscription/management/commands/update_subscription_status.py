from typing import Any

from django.core.management.base import BaseCommand
from django.utils import timezone
from subscription.models import Status, Subscription


class Command(BaseCommand):
    help = "Update subscriptions status..."

    def handle(self, *args: Any, **options: Any) -> None:
        self.update_subscription_status()

        self.stdout.write(
            self.style.SUCCESS("Successfully updated subscriptions status.")
        )

    @staticmethod
    def update_subscription_status() -> None:
        subscriptions = Subscription.objects.all()
        for subscription in subscriptions:
            subscription_is_active = (
                subscription.start_date
                <= timezone.now().date()
                <= subscription.end_date
            )
            payment_is_completed = subscription.payment.status == Status.COMPLETED
            subscription.is_active = subscription_is_active and payment_is_completed
            subscription.save()
