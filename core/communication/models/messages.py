from django.conf import settings
from django.db import models
from django.utils import timezone


class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages"
    )
    title = models.CharField(max_length=256, help_text="Title of the message")
    content = models.TextField(help_text="Content of the message")
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(
        default=False, help_text="Whether the message is read"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"{self.user} - {self.title}"
