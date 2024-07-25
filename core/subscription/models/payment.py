from django.db import models
from subscription.models import Subscription


class Payment(models.Model):
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Enter payment amount"
    )
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, help_text="Enter subscription"
    )
    date = models.DateField(auto_now_add=True, help_text="Enter date of payment")

    class Meta:
        ordering = ["-date"]
