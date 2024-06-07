from django.urls import path

from .views import RunningCostDeleteMultipleView, RunningCostUpdateView, RunningCostView

app_name = "running-costs"

urlpatterns = [
    path("list/", RunningCostView.as_view(), name="running-costs-list"),
    path(
        "list/<int:pk>/update/",
        RunningCostUpdateView.as_view(),
        name="running-costs-detail-update",
    ),
    path(
        "list/delete-multiple/",
        RunningCostDeleteMultipleView.as_view(),
        name="running-costs-list-delete-multiple",
    ),
]
