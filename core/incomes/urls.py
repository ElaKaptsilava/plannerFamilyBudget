from django.urls import path

from .views import GetIncomesView, IncomesView

app_name = "incomes"

urlpatterns = [
    path("incomes/", GetIncomesView.as_view(), name="incomes"),  # income-list
    path(
        "incomes/create/", IncomesView.as_view(), name="create_income"
    ),  # income-list-create
    path(
        "incomes/<int:income_pk>/delete/",
        IncomesView.as_view(),
        name="income_delete",  # income-detail-delete
    ),
    path(
        "incomes/<int:income_pk>/update/",
        IncomesView.as_view(),
        name="income_update",  # income-detail-update
    ),
]
