from django.core.management import BaseCommand
from django.db import models
from django.utils import timezone
from targets.models import Target


class Command(BaseCommand):
    help = "Update deadlines for targets that are not completed and have a deadline greater than the current date."

    def handle(self, *args, **options):
        targets = Target.objects.filter(
            is_completed=models.Value(False),
            total_amount__lt=models.F("amount"),
            deadline__lte=timezone.now().date(),
        )
        for target in targets:
            target.update_deadline()

        self.stdout.write(
            self.style.SUCCESS("Successfully updated deadlines for targets.")
        )
