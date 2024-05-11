from django.urls import path

from .views import CustomLoginView, RegisterView, log_in

app_name = "accounts"

urlpatterns = [
    path("login-user/", log_in, name="login"),
    path("customlogin/", CustomLoginView.as_view(), name="customlogin"),
    path("register/", RegisterView.as_view(), name="register"),
]
