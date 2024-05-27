from django.urls import path

from . import views

app_name = "expenses"

urlpatterns = [
    path("", views.ExpenseView.as_view(), name="expenses-list"),
    path(
        "<int:pk>/update/",
        views.ExpensesUpdateView.as_view(),
        name="expenses-detail-update",
    ),
    path(
        "delete-multiple/",
        views.DeleteMultipleExpenseView.as_view(),
        name="expenses-list-delete-multiple",
    ),
]
