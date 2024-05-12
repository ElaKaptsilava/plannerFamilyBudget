from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(get_user_model().USERNAME_FIELD)
            print(username)
        try:
            case_insensitive_user = "{}__iexact".format(get_user_model().USERNAME_FIELD)
            user = get_user_model().__default_manager.get(
                **{case_insensitive_user: username}
            )
        except get_user_model().DoesNotExist:
            get_user_model().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


# class EmailAuthBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         try:
#             user = CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             return None
#
#         if user.check_password(password):
#             return user
