from accounts.models import CustomUser
from django.db import models
from PIL import Image

DEFAULT_PROFILE_IMAGE = "undraw_profile.svg"


def get_upload_path(self, instance, filename):
    folder_name = f"{instance.email}_{instance.id}"
    return "/".join(["accounts", folder_name, filename])


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
