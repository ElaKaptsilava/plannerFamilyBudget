from budgets_manager.views.budget import create_view
from django.urls import path

app_name = "manager"
urlpatterns = [
    path(
        "<int:user_id>/budget/create/",
        create_view.BudgetManagerFormView.as_view(),
        name="budget-list-create",
    ),
]
