from django.urls import path

from . import views

app_name = "running-costs"

urlpatterns = [
    path("", views.RunningCostView.as_view(), name="running-costs-list"),
    path(
        "<int:pk>/update/",
        views.RunningCostView.as_view(),
        name="running-costs-detail-update",
    ),
]
