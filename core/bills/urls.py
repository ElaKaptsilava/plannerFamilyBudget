from django.urls import path

from . import views

app_name = "bills"

urlpatterns = [
    path("list/", views.BillFormView.as_view(), name="bills-list"),
]
