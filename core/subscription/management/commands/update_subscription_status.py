from typing import Any

from django.core.management.base import BaseCommand
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
            if subscription.payment.status == Status.COMPLETED:
                subscription.update_status()
                subscription.save()
