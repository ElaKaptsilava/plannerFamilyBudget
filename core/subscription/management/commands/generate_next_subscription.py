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
            if hasattr(user, "subscription"):
                if user.subscription.end_date == timezone.now():
                    Subscription.objects.create(user=user, plan=user.subscription.plan)
