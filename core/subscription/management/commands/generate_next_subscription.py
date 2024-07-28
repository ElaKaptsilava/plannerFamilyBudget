import typing

from accounts.models import CustomUser
from django.core.management.base import BaseCommand
from django.utils import timezone
from subscription.models import Subscription


class Command(BaseCommand):
    help = "Generate next subscription."

    def handle(self, *args: typing.Any, **options: typing.Any) -> None:
        self.generate_next_subscription()

        self.stdout.write("Successfully generating next subscription...")

    @staticmethod
    def generate_next_subscription() -> None:
        for user in CustomUser.objects.all():
            if user.subscription_set.exists():
                last_subscription = user.subscription_set.latest("end_date")
                if (
                    last_subscription.end_date == timezone.now().date()
                    and last_subscription.is_active
                ):
                    Subscription.objects.create(user=user, plan=last_subscription.plan)
