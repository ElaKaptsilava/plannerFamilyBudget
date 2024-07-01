from typing import Union

from accounts.models import get_upload_path
from django.conf import settings
from django.db import models
from django.utils import timezone

from core.constants import labels


class Target(models.Model):
    today = timezone.now().date()
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
    def is_completed(self) -> bool:
        return self.total_contributions >= self.amount

    @property
    def total_contributions(self) -> float:
        return (
            self.targetcontribution_set.aggregate(total=models.Sum("amount"))["total"]
            or 0.0
        )

    @property
    def progress_percentage(self) -> Union[int, float]:
        return int(self.total_contributions * 100 / self.amount)

    def update_deadline(self) -> None:
        self.deadline += timezone.timedelta(days=30)
        self.save()

    def calculate_months(self, today) -> int:
        months = (
            (self.deadline.year - today.year) * 12 + self.deadline.month - today.month
        )
        return int(months)

    @property
    def monthly_payment(self) -> float:
        months = self.calculate_months(self.today)
        if months > 0 and not self.is_completed:
            remaining_amount = self.amount - self.total_contributions
            return round(remaining_amount / months, 2)
        return 0.0

    @property
    def deadline_is_overdue(self) -> bool:
        return self.deadline <= self.today

    @property
    def deadline_status_label(self) -> str:
        if self.deadline_is_overdue:
            return labels.SUCCESS
        return labels.DANGER

    @property
    def completed_status_label(self) -> str:
        if self.is_completed:
            return labels.SUCCESS
        if self.progress_percentage < 80:
            return labels.INFO
        return labels.WARNING
