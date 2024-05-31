from django.urls import path

from . import views

app_name = "targets"
urlpatterns = [
    path("list/", views.TargetView.as_view(), name="targets-list"),
]
