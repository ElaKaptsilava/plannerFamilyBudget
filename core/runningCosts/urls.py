from django.urls import path

from .views import RunningCostView

app_name = "running-costs"

urlpatterns = [
    path("", RunningCostView.as_view(), name="running-costs-list"),
    path(
        "<int:pk>/update/",
        RunningCostView.as_view(),
        name="running-costs-detail-update",
    ),
]
