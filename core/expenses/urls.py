from django.urls import path
from expenses.views.expence import (
    expense_formview,
    expense_update,
    expense_multiple_delete,
)

app_name = "expenses"

urlpatterns = [
    path("", expense_formview.ExpenseView.as_view(), name="expenses-list"),
    path(
        "<int:pk>/update/",
        expense_update.ExpensesUpdateView.as_view(),
        name="expenses-detail-update",
    ),
    path(
        "delete-multiple/",
        expense_multiple_delete.DeleteMultipleExpenseView.as_view(),
        name="expenses-list-delete-multiple",
    ),
]
