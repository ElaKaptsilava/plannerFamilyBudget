from django.db import models
from multi_user.models.collabaration import Collaboration


class Invitation(models.Model):
    collaboration = models.ForeignKey(
        Collaboration, on_delete=models.CASCADE, help_text="Enter collaborations..."
    )
    email = models.EmailField(help_text="Enter Email")
    token = models.CharField(max_length=100, unique=True, help_text="Token")
    accepted = models.BooleanField(default=False, help_text="Is accepted...")

    def __str__(self) -> str:
        return f"Invite to {self.collaboration} for {self.email}"

    def __repr__(self) -> str:
        return f"Invitation(collaboration={self.collaboration}, email={self.email}, accepted={self.accepted})"
