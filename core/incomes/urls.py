from django.urls import path

from .views import IncomesView

app_name = "incomes"

urlpatterns = [
    path("create-income/", IncomesView.as_view(), name="create-income"),
]
