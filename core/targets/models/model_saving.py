from django.conf import settings
from django.db import models


class Saving(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
