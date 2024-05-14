from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


def get_upload_path(instance, filename):
    return "/".join(["accounts", str(instance.id), filename])


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


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
    )
    avatar = models.ImageField(default="undraw_profile.svg", upload_to=get_upload_path)

    def __str__(self):
        return f"{self.user.first_name} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar.name != "undraw_profile.svg":
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
