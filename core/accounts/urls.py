from django.contrib.auth import views as auth_views
from django.urls import path

from . import views as accounts_views

app_name = "accounts"

urlpatterns = [
    path("login/", accounts_views.login_view, name="login"),
    path("register/", accounts_views.register_view, name="register"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="registration/logged_out.html"),
        name="logout",
    ),
    path("profile/<int:user_id>", accounts_views.ProfileView.as_view(), name="profile"),
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "reset-password/",
        accounts_views.CustomResetPasswordView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        accounts_views.CustomResetPasswordConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        accounts_views.CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
