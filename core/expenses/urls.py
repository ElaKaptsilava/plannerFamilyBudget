from django.urls import path
from expenses.views.category_expense import (
    category_create,
    category_delete,
    category_list,
    category_update,
)
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
    path(
        "category/update/<int:pk>/",
        category_update.CategoryExpenseUpdateView.as_view(),
        name="category-detail-update",
    ),
    path(
        "category/<int:pk>/delete/",
        category_delete.CategoryExpenseDeleteView.as_view(),
        name="category-detail-delete",
    ),
]
