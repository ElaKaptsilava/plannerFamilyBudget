from django.urls import path
from expenses.views import ExpenseListView

app_name = "expenses"

urlpatterns = [
    path("list/", ExpenseListView.as_view(), name="expenses-list"),
]
