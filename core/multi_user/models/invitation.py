import uuid

from budgets_manager.models import BudgetManager
from django.db import models


class InvitationToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    budget = models.ForeignKey(BudgetManager, on_delete=models.CASCADE)
    email = models.EmailField(help_text="Email of the person invited")
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation Token for {self.email} - Used: {self.is_used}"

    def __repr__(self):
        return f"InvitationToken(family_budget={self.budget!r}, email={self.email!r})"

    @staticmethod
    def create_token() -> uuid:
        return uuid.uuid4()
