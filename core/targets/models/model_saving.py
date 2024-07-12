from django.conf import settings
from django.db import models


class Saving(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saving"
    )
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
        amount = 0.0
        contributions = self.savingcontributions_set.all()
        if contributions:
            amount = contributions.aggregate(
                amount=models.Sum("amount"),
            )["amount"]
        return amount


# models.DecimalField
class SavingContributions(models.Model):
    amount = models.DecimalField(
        default=0.0,
        decimal_places=2,
        max_digits=10,
        verbose_name="Amount",
        help_text="Enter the amount.",
    )
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE, verbose_name="Saving")
    date = models.DateField(
        help_text="Date of the contribution entry.", auto_now_add=True
    )

    class Meta:
        ordering = ("date",)
