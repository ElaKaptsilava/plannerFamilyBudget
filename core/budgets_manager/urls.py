from budgets_manager.views.budget.create import BudgetManagerCreateView
from budgets_manager.views.budget.update import UpdateBudgetView
from budgets_manager.views.limits.create import LimitCreateView
from budgets_manager.views.limits.list import LimitListView
from budgets_manager.views.limits.multiple_delete import PlannerMultipleDeleteView
from django.urls import path

app_name = "manager"
urlpatterns = [
    path(
        "<int:user_id>/budget/create/",
        BudgetManagerCreateView.as_view(),
        name="budget-list-create",
    ),
    path(
        "budget/detail/<int:pk>/update/",
        UpdateBudgetView.as_view(),
        name="budget-detail-update",
    ),
    path(
        "<int:user_id>/planner/list/",
        LimitListView.as_view(),
        name="limits-list",
    ),
    path(
        "<int:user_id>/planner/list/create/",
        LimitCreateView.as_view(),
        name="limits-list-create",
    ),
    path(
        "<int:user_id>/planner/list/delete/multiple/",
        PlannerMultipleDeleteView.as_view(),
        name="limits-delete-multiple",
    ),
]
