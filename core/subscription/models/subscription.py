from accounts.models import CustomUser
from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from subscription.models import Plan, Status


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
        null=True, blank=True, help_text="The date when the subscription started."
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="The date when the subscription ends. Automatically set to 30 days from the start date if not "
        "specified.",
    )
    is_active = models.BooleanField(null=True, default=False, blank=True)

    class Meta:
        ordering = ["-end_date"]
        get_latest_by = "end_date"

    def __repr__(self) -> str:
        return (
            f"Subscription(user={self.user}, plan={self.plan}, "
            f"start_date={self.start_date}, end_date={self.end_date})"
        )

    def __str__(self) -> str:
        return f"Subscription for {self.user} to {self.plan} from {self.start_date} to {self.end_date}"

    def save(self, *args, **kwargs):
        if not self.start_date:
            queryset = self.user.subscription_set.all()
            self.start_date = timezone.now().date()
            if queryset.exists():
                self.start_date = queryset.first().end_date + relativedelta(days=1)
            self.end_date = self.start_date + relativedelta(months=1)
        super().save(*args, **kwargs)

    def check_is_active(self):
        if self.start_date and self.end_date:
            if self.payment and self.payment.status == Status.COMPLETED:
                self.is_active = True
            else:
                self.is_active = False
            self.save()
