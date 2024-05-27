from django.urls import path

from .views import DeleteMultipleIncomesView, IncomesListView, IncomesView

app_name = "incomes"

urlpatterns = [
    path("", IncomesListView.as_view(), name="incomes-list"),
    path("create/", IncomesView.as_view(), name="income-list-create"),
    path(
        "<int:pk>/update/",
        IncomesView.as_view(),
        name="income-detail-update",
    ),
    path(
        "delete-multiple/",
        DeleteMultipleIncomesView.as_view(),
        name="delete-multiple",
    ),
]
