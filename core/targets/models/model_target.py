from typing import Union

from accounts.models import get_upload_path
from django.conf import settings
from django.db import models
from django.utils import timezone


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

    def __str__(self) -> str:
        return f"{self.user.username}'s target: {self.target}"

    @property
    def total_contributions(self):
        return (
            self.targetcontribution_set.aggregate(total=models.Sum("amount"))["total"]
            or 0
        )

    @property
    def progress_percentage(self) -> Union[int, float]:
        return int(self.total_contributions * 100 / self.amount)
