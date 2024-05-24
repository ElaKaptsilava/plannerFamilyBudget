from accounts.models import CustomUser
from django.db import models


class RunningCostCategory(models.Model):
    name = models.CharField(
        max_length=256, help_text="Enter the category of the running coast."
    )
    description = models.TextField(
        null=True, blank=True, help_text="Enter the category description."
    )

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"RunningCostCategory(name={self.name!r}, description={self.description[:10]!r}...)"


class RunningCost(models.Model):
    class PeriodType(models.TextChoices):
        DAYS = ("days", "Days")
        WEEKS = ("weeks", "Weeks")
        MONTHS = ("months", "Months")
        YEARS = ("years", "Years")

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="running_costs"
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
        help_text="The number of periods (e.g., 2 for bi-monthly)."
    )
    due_date = models.DateField(help_text="The due date for the next payment.")

    def __str__(self) -> str:
        return f"{self.name} - ${self.amount:.2f}"

    def __repr__(self) -> str:
        return (
            f"RunningCost(name={self.name!r}, period=({self.period_type!r}, {self.period!r}), "
            f"amount={self.amount!r}, due date={self.due_date})"
        )
