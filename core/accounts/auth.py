import os

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(get_user_model().USERNAME_FIELD)
        try:
            case_insensitive_user = "{}__iexact".format(get_user_model().USERNAME_FIELD)
            user = get_user_model().objects.get(**{case_insensitive_user: username})
        except get_user_model().DoesNotExist:
            get_user_model().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class FileBasedEmailBackend:
    def __init__(self, file_path=None):
        if file_path is None:
            raise ValueError("A valid file path is required for the email backend.")
        else:
            self.file_path = os.path.abspath(file_path)
