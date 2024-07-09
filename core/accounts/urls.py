from accounts.views.authorization import (
    CustomLoginView,
    CustomRegisterView,
    CustomResetPasswordView,
)
from accounts.views.profile import ProfileView
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", CustomRegisterView.as_view(), name="register"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="registration/logged_out.html"),
        name="logout",
    ),
    path("profile/<int:user_id>/", ProfileView.as_view(), name="profile"),
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
        CustomResetPasswordView.as_view(),
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
