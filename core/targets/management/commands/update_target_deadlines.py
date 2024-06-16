from django.core.management import BaseCommand
from django.utils import timezone
from targets.models import Target


class Command(BaseCommand):
    help = "Update deadlines for targets that are not completed and have a deadline greater than the current date."

    def handle(self, *args, **options):
        targets = Target.objects.filter(deadline__lte=timezone.now().date())
        for target in targets:
            if not target.is_completed:
                target.update_deadline()

        self.stdout.write(
            self.style.SUCCESS("Successfully updated deadlines for targets.")
        )
