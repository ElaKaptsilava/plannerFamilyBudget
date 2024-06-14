from budgets_manager.views.planner import (
    planner_create,
    planner_list,
    planner_multiple_delete,
)
from budgets_manager.views.budget import budget_create, budget_update
from django.urls import path

app_name = "manager"
urlpatterns = [
    path(
        "<int:user_id>/budget/create/",
        budget_create.BudgetManagerCreateView.as_view(),
        name="budget-list-create",
    ),
    path(
        "budget/detail/<int:pk>/update/",
        budget_update.UpdateBudgetView.as_view(),
        name="budget-detail-update",
    ),
    path(
        "<int:user_id>/planner/list/",
        planner_list.PlannerListView.as_view(),
        name="planner-list",
    ),
    path(
        "<int:user_id>/planner/list/create/",
        planner_create.PlannerCreateView.as_view(),
        name="planner-list-create",
    ),
    path(
        "<int:user_id>/planner/list/delete/multiple/",
        planner_multiple_delete.PlannerMultipleDeleteView.as_view(),
        name="planner-delete-multiple",
    ),
]
