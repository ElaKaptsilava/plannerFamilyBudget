from django.urls import path

from .views import DeleteMultipleIncomesView, IncomesListView, IncomesView

app_name = "incomes"

urlpatterns = [
    path("incomes/", IncomesListView.as_view(), name="incomes-list"),
    path("incomes/", IncomesView.as_view(), name="income-list-create"),
    path(
        "incomes/<int:pk>/update/",
        IncomesView.as_view(),
        name="income-detail-update",
    ),
    path(
        "delete-multiple/", DeleteMultipleIncomesView.as_view(), name="delete-multiple"
    ),
]
