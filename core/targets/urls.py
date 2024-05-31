from django.urls import path

from . import views

app_name = "targets"
urlpatterns = [
    path("list/", views.TargetListView.as_view(), name="targets-list"),
]
