from typing import Union

from accounts.models import UserAbstractModel, get_upload_path
from django.db import models
from django.utils import timezone


class Saving(UserAbstractModel):
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, help_text="Amount saved."
    )
    date = models.DateField(help_text="Date of the saving entry.")

    def __str__(self) -> str:
        return f"{self.user.username} - Saving: {self.amount} on {self.date}"

    def __repr__(self) -> str:
        return (
            f"Saving(user={self.user.username!r}, amount={self.amount!r}, "
            f"date={self.date!r})"
        )


class Target(UserAbstractModel):
    image = models.ImageField(
        upload_to=get_upload_path, default="/static/img/undraw_posting_photo.svg"
    )
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


class TargetContribution(UserAbstractModel):
    target = models.ForeignKey(
        Target,
        on_delete=models.CASCADE,
        help_text="The target this contribution is associated with.",
    )
    amount = models.FloatField(
        help_text="The amount of money contributed towards the target."
    )
    date = models.DateField(
        auto_now_add=True,
        help_text="The date when the contribution was made. Automatically set to the current date.",
    )

    class Meta:
        ordering = ("-date",)

    def __str__(self) -> str:
        return f"Income for {self.target} on {self.date}"
