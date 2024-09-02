from django.urls import path
from expenses.views.category_expense import (
    CategoryCreateView,
    CategoryExpenseDeleteView,
    CategoryExpenseUpdateView,
    CategoryListView,
)
from expenses.views.expence import (
    DeleteMultipleExpenseView,
    ExpensesCreateView,
    ExpensesListView,
    ExpensesUpdateView,
)

app_name = "expenses"

urlpatterns = [
    path("list/", ExpensesListView.as_view(), name="expenses-list"),
    path("list/create/", ExpensesCreateView.as_view(), name="expenses-list-create"),
    path(
        "<int:pk>/update/",
        ExpensesUpdateView.as_view(),
        name="expenses-detail-update",
    ),
    path(
        "delete-multiple/",
        DeleteMultipleExpenseView.as_view(),
        name="expenses-list-delete-multiple",
    ),
    path("category/list/", CategoryListView.as_view(), name="category-list"),
    path(
        "category/create/",
        CategoryCreateView.as_view(),
        name="category-list-create",
    ),
    path(
        "category/update/<int:pk>/",
        CategoryExpenseUpdateView.as_view(),
        name="category-detail-update",
    ),
    path(
        "category/<int:pk>/delete/",
        CategoryExpenseDeleteView.as_view(),
        name="category-detail-delete",
    ),
]
