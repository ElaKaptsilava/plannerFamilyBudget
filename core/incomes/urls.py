from django.urls import path

from .views import DeleteMultipleIncomesView, GetIncomesView, IncomesView

app_name = "incomes"

urlpatterns = [
    path("incomes/", GetIncomesView.as_view(), name="incomes-list"),
    path("incomes/create/", IncomesView.as_view(), name="income-list-create"),
    path(
        "incomes/<int:pk>/update/",
        IncomesView.as_view(),
        name="income-detail-update",
    ),
    path(
        "delete-multiple/", DeleteMultipleIncomesView.as_view(), name="delete-multiple"
    ),
]
