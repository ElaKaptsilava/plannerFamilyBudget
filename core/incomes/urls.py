from django.urls import path

from .views import GetIncomesView, IncomesView

app_name = "incomes"

urlpatterns = [
    path("incomes/", GetIncomesView.as_view(), name="incomes-list"),
    path("incomes/create/", IncomesView.as_view(), name="income-list-create"),
    path(
        "incomes/<int:income_pk>/delete/",
        IncomesView.as_view(),
        name="income-detail-delete",
    ),
    path(
        "incomes/<int:pk>/update/",
        IncomesView.as_view(),
        name="income-detail-update",
    ),
]
