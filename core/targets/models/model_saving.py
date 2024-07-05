from django.conf import settings
from django.db import models


class Saving(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(help_text="Date of the saving entry.", auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} - Saving: {self.total_amount} on {self.date}"

    def __repr__(self) -> str:
        return (
            f"Saving(user={self.user!r}, amount={self.total_amount!r}, "
            f"date={self.date!r})"
        )

    @property
    def total_amount(self) -> float:
        return (
            self.savingcontributions_set.all().aggregate(total=models.Sum("amount"))[
                "total"
            ]
            or 0.0
        )


class SavingContributions(models.Model):
    amount = models.FloatField(default=0, verbose_name="Savings amount")
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE, verbose_name="Saving")
