from django.urls import path

from .views.category_expense.create import CategoryCreateView
from .views.category_expense.delete import CategoryExpenseDeleteView
from .views.category_expense.list import CategoryListView
from .views.category_expense.update import CategoryExpenseUpdateView
from .views.expence import ExpensesCreateView, ExpensesListView
from .views.expence.multiple_delete import DeleteMultipleExpenseView
from .views.expence.update import ExpensesUpdateView

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
