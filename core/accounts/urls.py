from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views as accounts_views

app_name = "accounts"

urlpatterns = [
    path("login/", accounts_views.CustomLoginView.as_view(), name="login"),
    path("register/", accounts_views.CustomRegisterView.as_view(), name="register"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="registration/logged_out.html"),
        name="logout",
    ),
    path(
        "profile/<int:user_id>/", accounts_views.ProfileView.as_view(), name="profile"
    ),
    path(
        "password-change/<int:user_id>/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change.html",
            success_url=reverse_lazy("accounts:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "reset-password/",
        accounts_views.CustomResetPasswordView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/reset_password_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
