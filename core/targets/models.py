from accounts.models import CustomUser, get_upload_path
from django.db import models
from django.utils import timezone


class Target(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=get_upload_path, default="/static/img/undraw_posting_photo.svg"
    )
    target = models.CharField(max_length=255, help_text="A name of the target goal.")
    amount = models.FloatField(
        help_text="The amount of money required to achieve the target."
    )
    deadline = models.DateField(
        default=timezone.now,
        help_text="The deadline for achieving the target. Defaults to one year from now.",
    )
    description = models.TextField(
        help_text="A description of the target.", null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s target: {self.target}"


class TargetContribution(models.Model):
    target = models.ForeignKey(
        Target,
        on_delete=models.CASCADE,
        help_text="The target this contribution is associated with.",
    )
    amount = models.FloatField(
        help_text="The amount of money contributed towards the target."
    )
    date = models.DateField(
        auto_now_add=True,
        help_text="The date when the contribution was made. Automatically set to the current date.",
    )

    def __str__(self):
        return f"Income for {self.target} on {self.date}"
