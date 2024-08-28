import uuid

from accounts.models import CustomUser
from django.db import models


class Collaboration(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, help_text="User to collaborate"
    )
    token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="Unique token for user",
    )

    class Meta:
        ordering = ["user"]

    def __str__(self) -> str:
        return f"Collaboration for {self.user}"

    def __repr__(self) -> str:
        return f"Collaboration for {self.user}"

    def clean(self):
        while Collaboration.objects.filter(token=self.token).exists():
            self.token = uuid.uuid4()
        super().clean()
