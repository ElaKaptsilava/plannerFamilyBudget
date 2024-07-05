import calendar
from datetime import date, datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class RunningCostQuerySet(models.QuerySet):
    def with_active(self) -> bool:
        return self.annotate(
            is_late_payment=models.Case(
                models.When(
                    payment_deadline__lte=timezone.now(),
                    is_paid=False,
                    then=models.Value(True),
                ),
                default=models.Value(False),
                output_field=models.BooleanField(),
            )
        )


class RunningCostCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=256, help_text="Enter the category of the running coast."
    )
    description = models.TextField(
        null=True, blank=True, help_text="Enter the category description."
    )

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"RunningCostCategory(name={self.name!r}, description={self.description!r}...)"


class RunningCost(models.Model):
    class PeriodType(models.TextChoices):
        MONTHS = ("months", "Months")
        YEARS = ("years", "Years")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="running_costs"
    )

    name = models.CharField(max_length=256)
    category = models.ForeignKey(
        RunningCostCategory, on_delete=models.CASCADE, related_name="running_costs"
    )
    amount = models.FloatField(help_text="The amount of money for the running cost.")
    period_type = models.CharField(
        max_length=256,
        choices=PeriodType.choices,
        default=PeriodType.MONTHS,
        help_text="The type of period for the running cost (e.g., months, weeks).",
    )
    period = models.PositiveSmallIntegerField(
        help_text="The number of periods (e.g., 2 for bi-monthly).",
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    payment_deadline = models.DateField(
        default=timezone.now, help_text="The deadline for paying the running cost."
    )
    is_paid = models.BooleanField(
        default=False,
        help_text="Indicates whether the running cost has been paid or not.",
    )
    next_payment_date = models.DateField(
        null=True, blank=True, help_text="The next scheduled payment date."
    )
    objects = RunningCostQuerySet.as_manager()

    class Meta:
        ordering = ["next_payment_date"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["next_payment_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} - ${self.amount:.2f}"

    def __repr__(self) -> str:
        return (
            f"RunningCost(name={self.name!r}, period=({self.period_type!r}, {self.period!r}), "
            f"amount={self.amount!r}, payment day={self.next_payment_date})"
        )

    def save(self, *args, **kwargs) -> None:
        if self.is_paid:
            self.update_next_payment_date()
        super().save(*args, **kwargs)

    @property
    def has_overdue(self) -> bool:
        if hasattr(self, "is_late_payment"):
            return self.is_late_payment
        today = timezone.now().date()
        return today > self.next_payment_date and not self.is_paid

    @property
    def is_completed(self) -> bool:
        if not self.next_payment_date:
            return True
        return False

    @property
    def total_amount_in_month(self) -> int:
        calculate_total = {
            self.PeriodType.MONTHS: round(self.amount / self.period),
            self.PeriodType.YEARS: round(self.amount / self.period * 12),
        }
        if self.is_completed:
            return 0
        return calculate_total.get(self.period_type, 0)

    def update_next_payment_date(self) -> None:
        conditions = {
            self.PeriodType.MONTHS: self.add_months(
                self.next_payment_date, self.period
            ),
            self.PeriodType.YEARS: self.add_years(self.next_payment_date, self.period),
        }
        next_payment_date = conditions.get(self.period_type)

        if isinstance(self.payment_deadline, datetime):
            payment_deadline = self.payment_deadline.date()
        else:
            payment_deadline = self.payment_deadline

        if next_payment_date < payment_deadline:
            self.next_payment_date = next_payment_date
        else:
            self.next_payment_date = None

    @staticmethod
    def add_months(source_date: date, period: int) -> date:
        month = source_date.month + period
        year = source_date.year
        if month > 12:
            month -= 12
            year += 1
        day = min(source_date.day, calendar.monthrange(year, month)[1])
        return date(year, month, day)

    @staticmethod
    def add_years(source_date: date, period: int) -> date:
        try:
            return source_date.replace(year=source_date.year + period)
        except ValueError:
            return source_date.replace(month=2, day=28, year=source_date.year + period)
