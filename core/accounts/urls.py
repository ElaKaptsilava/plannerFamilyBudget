from django.urls import path
from django.views.generic import TemplateView

from .views import CustomLoginView, register_view

app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", register_view, name="register"),
    path("", TemplateView.as_view(template_name="accounts/index.html"), name="home"),
]
