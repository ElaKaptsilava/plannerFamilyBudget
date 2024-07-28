from django.db import models
from django.utils import timezone


class Status(models.TextChoices):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"


class Payment(models.Model):
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Enter payment amount"
    )
    subscription = models.OneToOneField(
        "Subscription", on_delete=models.CASCADE, help_text="Enter subscription"
    )
    due_date = models.DateField(default=timezone.now, help_text="Enter date of payment")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        help_text="Status of the payment",
    )

    class Meta:
        ordering = ["-due_date"]

    def __str__(self) -> str:
        return f"{self.amount} {self.subscription}"

    def __repr__(self) -> str:
        return f"<Payment: {self.amount} {self.subscription}>"
