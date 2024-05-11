from django.urls import path

from .views import RegisterView, login_view

app_name = "accounts"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", RegisterView.as_view(), name="register"),
]
