from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
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
        amount = self.savingcontributions_set.all().aggregate(
            positive_amount=models.Sum("positive_amount"),
            negative_amount=models.Sum("negative_amount"),
        )
        return sum(amount.values())


class SavingContributions(models.Model):
    positive_amount = models.FloatField(
        default=0,
        verbose_name="Positive amount",
        help_text="Amount of the positive amount.",
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
    )
    negative_amount = models.FloatField(
        default=0,
        verbose_name="Negative amount",
        help_text="Amount of the negative amount.",
        null=True,
        blank=True,
        validators=[MaxValueValidator(0)],
    )
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE, verbose_name="Saving")
