from django.urls import path
from runningCosts.views.category import (
    CategoryCostDeleteView,
    CategoryCostUpdateView,
    CategoryCreateView,
    CategoryListView,
)
from runningCosts.views.running_cost import (
    RunningCostDeleteMultipleView,
    RunningCostUpdateView,
    RunningCostView,
)

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
    path(
        "category/list/",
        CategoryListView.as_view(),
        name="category-list",
    ),
    path(
        "category/list/create/",
        CategoryCreateView.as_view(),
        name="category-list-create",
    ),
    path(
        "category/detail/<int:pk>/update/",
        CategoryCostUpdateView.as_view(),
        name="category-detail-update",
    ),
    path(
        "category/detail/<int:pk>/delete/",
        CategoryCostDeleteView.as_view(),
        name="category-detail-delete",
    ),
]
