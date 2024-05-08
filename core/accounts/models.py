from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'username']

    def __str__(self) -> str:
        return f'{self.email}'

    def __repr__(self) -> str:
        return f'CustomUser(email={self.email!r})'
