from datetime import timedelta

from accounts.models import CustomUser
from django.db import models
from django.utils import timezone
from subscription.models import Plan


class Subscription(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        help_text="The user who owns this subscription.",
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        help_text="The subscription plan selected by the user.",
    )
    start_date = models.DateField(
        auto_now_add=True, help_text="The date when the subscription started."
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="The date when the subscription ends. Automatically set to 30 days from the start date if not specified.",
    )

    class Meta:
        ordering = ["-end_date"]

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=30)
        super().save(*args, **kwargs)

    def __repr__(self) -> str:
        return f"{self.user} - {self.plan}"

    def __str__(self) -> str:
        return f"{self.plan} - {self.end_date}"

    def is_active(self) -> bool:
        if not self.end_date:
            return False
        return self.end_date > timezone.now()
