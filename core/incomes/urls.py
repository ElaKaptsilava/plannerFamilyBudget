from django.urls import path

from .views import GetIncomesView, IncomesView

app_name = "incomes"

urlpatterns = [
    path("incomes/create/", IncomesView.as_view(), name="create_income"),
    path("incomes/", GetIncomesView.as_view(), name="incomes"),
    path(
        "incomes/<int:income_pk>/delete/", IncomesView.as_view(), name="income_delete"
    ),
]
