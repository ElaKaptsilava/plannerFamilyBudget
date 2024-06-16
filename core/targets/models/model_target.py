from typing import Union

from accounts.models import get_upload_path
from django.conf import settings
from django.db import models
from django.utils import timezone


class TargetQuerySet(models.QuerySet):
    def with_total_contributions(self):
        return self.annotate(total_amount=models.Sum("targetcontribution__amount"))

    def with_completed(self):
        return self.annotate(
            is_completed=models.Case(
                models.When(
                    total_contributions__gte=models.F("amount"), then=models.Value(True)
                ),
                default=models.Value(False),
                output_field=models.BooleanField(),
            )
        )


class Target(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    target = models.CharField(max_length=255, help_text="A name of the target goal.")
    amount = models.FloatField(
        help_text="The amount of money required to achieve the target."
    )
    deadline = models.DateField(
        default=timezone.now,
        help_text="The deadline for achieving the target. Defaults to one year from now.",
    )
    description = models.TextField(
        help_text="A description of the target.", null=True, blank=True
    )

    objects = TargetQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.user.username}'s target: {self.target}"

    @property
    def status(self) -> bool:
        if hasattr(self, "is_completed"):
            return self.is_completed
        return False

    def update_deadline(self) -> None:
        if not self.status and self.deadline > timezone.now().date():
            self.deadline += timezone.timedelta(days=30)
            self.save()

    @property
    def total_contributions(self) -> float:
        if hasattr(self, "total_amount"):
            return self.total_amount
        return 0.0

    @property
    def progress_percentage(self) -> Union[int, float]:
        return int(self.total_contributions * 100 / self.amount)

    # @property
    # def saving_amount_in_month(self) -> int:
    #     amount_of_month = self.deadline - timezone.now().date()
    #     return
