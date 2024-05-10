from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, help_text="Email address")
    username = models.CharField(
        max_length=50,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.email}"

    def __repr__(self) -> str:
        return f"CustomUser(email={self.email!r})"
