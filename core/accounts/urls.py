import views as accounts_views
from django.contrib.auth import views as auth_views
from django.urls import path

app_name = "accounts"

urlpatterns = [
    path("login/", accounts_views.login_view, name="login"),
    path("register/", accounts_views.register_view, name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

reset_password_urls = [
    path(
        "password_reset/",
        accounts_views.MyPasswordResetView.as_view(),
        name="password-reset",
    ),
    # path('password_reset/done/', MyPasswordResetDoneView.as_view(), name='password-reset-done'),
    # path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    # path('reset/done/', MyPasswordResetCompleteView.as_view(), name='password-reset-complete'),
]

urlpatterns += reset_password_urls
