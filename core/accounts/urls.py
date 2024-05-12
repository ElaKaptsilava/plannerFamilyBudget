from django.contrib.auth import views as auth_views
from django.urls import path

from . import views as accounts_views

app_name = "accounts"

urlpatterns = [
    path("login/", accounts_views.login_view, name="login"),
    path("register/", accounts_views.register_view, name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password-reset/",
        accounts_views.CustomResetPasswordView.as_view(),
        name="reset-password",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password-reset-confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
]
