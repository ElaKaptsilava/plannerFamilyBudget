from django.urls import path
from runningCosts.views.running_cost.delete_multiple import (
    RunningCostDeleteMultipleView,
)
from runningCosts.views.running_cost.form_view import RunningCostView
from runningCosts.views.running_cost.update import RunningCostUpdateView

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
