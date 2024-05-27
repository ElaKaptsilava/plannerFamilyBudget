from django.urls import path

from . import views

app_name = "expenses"

urlpatterns = [
    path("list/", views.ExpenseListView.as_view(), name="expenses-list"),
    path("list/create/", views.ExpenseView.as_view(), name="expenses-list-create"),
    path(
        "list/delete-multiple/",
        views.DeleteMultipleExpenseView.as_view(),
        name="expenses-list-delete-multiple",
    ),
    path(
        "<int:pk>/update/", views.ExpenseView.as_view(), name="expenses-detail-update"
    ),
    path(
        "category/create/",
        views.ExpenseCategoryCreateView.as_view(),
        name="expenses-category-list-create",
    ),
]
