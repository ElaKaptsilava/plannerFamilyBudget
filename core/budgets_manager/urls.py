from budgets_manager.views.budget import (
    BudgetManagerCreateView,
    BudgetManagerListView,
    UpdateBudgetView,
)
from budgets_manager.views.limits import LimitCreateView, LimitListView
from budgets_manager.views.limits.multiple_delete import PlannerMultipleDeleteView
from django.urls import path

app_name = "manager"
urlpatterns = [
    path("budget/info/", BudgetManagerListView.as_view(), name="budget-info"),
    path(
        "budget/<int:user_id>/budget/create/",
        BudgetManagerCreateView.as_view(),
        name="budget-list-create",
    ),
    path(
        "budget/detail/<int:pk>/update/",
        UpdateBudgetView.as_view(),
        name="budget-detail-update",
    ),
    path(
        "<int:user_id>/limits/list/",
        LimitListView.as_view(),
        name="limits-list",
    ),
    path(
        "<int:user_id>/limits/list/create/",
        LimitCreateView.as_view(),
        name="limits-list-create",
    ),
    path(
        "<int:user_id>/limits/list/delete/multiple/",
        PlannerMultipleDeleteView.as_view(),
        name="limits-delete-multiple",
    ),
]
