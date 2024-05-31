import datetime

from accounts.models import CustomUser
from django.db import models
from django.utils import timezone


class Target(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    target = models.CharField(max_length=255, help_text="A name of the target goal.")
    amount = models.FloatField(
        help_text="The amount of money required to achieve the target."
    )
    deadline = models.DateField(
        default=lambda: timezone.now() + datetime.timedelta(days=365),
        help_text="The deadline for achieving the target. Defaults to one year from now.",
    )

    def __str__(self):
        return f"{self.user.username}'s target: {self.target}"


class TargetContribution(models.Model):
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

    def __str__(self):
        return f"Income for {self.target} on {self.date}"
