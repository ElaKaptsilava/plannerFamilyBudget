from django.urls import path
from incomes.views.incomes import (
    DeleteMultipleIncomesView,
    IncomesView,
    IncomeUpdateView,
)

app_name = "incomes"

urlpatterns = [
    path("", IncomesView.as_view(), name="incomes-list"),
    path(
        "<int:pk>/update/",
        IncomeUpdateView.as_view(),
        name="incomes-detail-update",
    ),
    path(
        "delete-multiple/",
        DeleteMultipleIncomesView.as_view(),
        name="incomes-delete-multiple",
    ),
]
