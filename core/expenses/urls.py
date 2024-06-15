from django.urls import path
from expenses.views.category_expense import category_create, category_list
from expenses.views.expence import (
    expense_formview,
    expense_multiple_delete,
    expense_update,
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
    path(
        "category/list/", category_list.CategoryListView.as_view(), name="category-list"
    ),
    path(
        "category/create/",
        category_create.CategoryCreateView.as_view(),
        name="category-list-create",
    ),
]
