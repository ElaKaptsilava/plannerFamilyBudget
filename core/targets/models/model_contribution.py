from django.conf import settings
from django.db import models
from targets.models import Target


class TargetContribution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
