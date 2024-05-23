from django.urls import path
from expenses.views import ExpenseCategoryCreateView, ExpenseListView, ExpenseView

app_name = "expenses"

urlpatterns = [
    path("list/", ExpenseListView.as_view(), name="expenses-list"),
    path("list/create/", ExpenseView.as_view(), name="expenses-list-create"),
    path(
        "category/create/",
        ExpenseCategoryCreateView.as_view(),
        name="expenses-category-list-create",
    ),
]
