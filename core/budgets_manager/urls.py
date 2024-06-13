from budgets_manager.views.budget import create_view, update_view
from budgets_manager.views.planner import list_view
from django.urls import path

app_name = "manager"
urlpatterns = [
    path(
        "<int:user_id>/budget/create/",
        create_view.BudgetManagerFormView.as_view(),
        name="budget-list-create",
    ),
    path(
        "budget/detail/<int:pk>/update/",
        update_view.UpdateBudgetView.as_view(),
        name="budget-detail-update",
    ),
    path(
        "<int:user_id>/planner/list/",
        list_view.PlanerListView.as_view(),
        name="planner-list",
    ),
]
