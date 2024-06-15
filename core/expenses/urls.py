from django.urls import path
from expenses.views.category_expense.create import CategoryCreateView
from expenses.views.category_expense.delete import CategoryExpenseDeleteView
from expenses.views.category_expense.list import CategoryListView
from expenses.views.category_expense.update import CategoryExpenseUpdateView
from expenses.views.expence.form_view import ExpensesView
from expenses.views.expence.multiple_delete import DeleteMultipleExpenseView
from expenses.views.expence.update import ExpensesUpdateView

app_name = "expenses"

urlpatterns = [
    path("list/", ExpensesView.as_view(), name="expenses-list"),
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
