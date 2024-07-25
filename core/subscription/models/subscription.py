from accounts.models import CustomUser
from django.db import models
from django.utils import timezone
from subscription.models import Plan


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        help_text="The user who owns this subscription.",
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        help_text="Select subscription plan.",
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

    def __repr__(self) -> str:
        return (
            f"Subscription(user={self.user}, plan={self.plan}, "
            f"start_date={self.start_date}, end_date={self.end_date})"
        )

    def __str__(self) -> str:
        return f"Subscription for {self.user} to {self.plan} from {self.start_date} to {self.end_date}"

    def is_active(self) -> bool:
        if not self.end_date:
            return False
        return self.end_date > timezone.now()
