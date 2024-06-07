from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image

DEFAULT_PROFILE_IMAGE = "undraw_profile.svg"


class UserAbstractModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True


def get_upload_path(self, instance, filename):
    folder_name = f"{instance.email}_{instance.id}"
    return "/".join(["accounts", folder_name, filename])


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, help_text="Email address")
    username = models.CharField(
        max_length=50,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["last_name", "first_name", "username"]

    def __str__(self) -> str:
        return f"{self.email}"

    def __repr__(self) -> str:
        return f"CustomUser(email={self.email!r})"


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
    )
    avatar = models.ImageField(default=DEFAULT_PROFILE_IMAGE, upload_to=get_upload_path)

    def __str__(self) -> str:
        return f"{self.user.first_name} Profile"

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

        if self.avatar.name == DEFAULT_PROFILE_IMAGE:
            return

        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
