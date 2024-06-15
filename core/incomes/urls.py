from django.urls import path
from incomes.views.incomes.delete_multiple import DeleteMultipleIncomesView
from incomes.views.incomes.form_view import IncomesView
from incomes.views.incomes.update import IncomeUpdateView

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
