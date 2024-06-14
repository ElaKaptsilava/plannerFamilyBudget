from django.urls import path

from runningCosts.views.running_cost import (
    cost_update,
    cost_formview,
    cost_delete_multiple,
)

app_name = "running-costs"

urlpatterns = [
    path("list/", cost_formview.RunningCostView.as_view(), name="running-costs-list"),
    path(
        "list/<int:pk>/update/",
        cost_update.RunningCostUpdateView.as_view(),
        name="running-costs-detail-update",
    ),
    path(
        "list/delete-multiple/",
        cost_delete_multiple.RunningCostDeleteMultipleView.as_view(),
        name="running-costs-list-delete-multiple",
    ),
]
