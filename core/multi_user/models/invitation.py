import uuid

from django.db import models
from multi_user.models import FamilyBudget


class InvitationToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    family_budget = models.ForeignKey(FamilyBudget, on_delete=models.CASCADE)
    email = models.EmailField(help_text="Email of the person invited")
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation Token for {self.email} - Used: {self.is_used}"

    def __repr__(self):
        return f"InvitationToken(family_budget={self.family_budget!r}, email={self.email!r})"

    @staticmethod
    def create_token() -> uuid:
        return uuid.uuid4()
