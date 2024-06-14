from django.urls import path

from incomes.views.incomes import income_update, income_formview, income_delete_multiple

app_name = "incomes"

urlpatterns = [
    path("", income_formview.IncomeView.as_view(), name="incomes-list"),
    path(
        "<int:pk>/update/",
        income_update.IncomeUpdateView.as_view(),
        name="incomes-detail-update",
    ),
    path(
        "delete-multiple/",
        income_delete_multiple.DeleteMultipleIncomesView.as_view(),
        name="incomes-delete-multiple",
    ),
]
