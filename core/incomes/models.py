from accounts.models import CustomUser
from django.db import models
from django.utils import timezone


class Income(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="incomes"
    )
    category = models.CharField(
        max_length=100,
        help_text="Enter the category of the income (e.g., salary, freelance)",
    )
    source = models.CharField(
        max_length=100,
        help_text="Enter the source of the income (e.g., employer, client)",
    )
    amount = models.FloatField(help_text="Enter the amount of the income")
    date = models.DateTimeField(
        default=timezone.now, help_text="Date and time when the income was recorded"
    )

    def __str__(self) -> str:
        return f"{self.user.username}'s {self.category} Income of {self.amount} recorded on {self.date}"

    def __repr__(self) -> str:
        return f"Income(user={self.user!s}, category={self.category!r},amount={self.amount!r}, date={self.date!r})"

    class Meta:
        ordering = ["-date"]
