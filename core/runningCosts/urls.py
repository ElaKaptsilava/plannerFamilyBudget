from django.urls import path

from . import views

app_name = "running-costs"

urlpatterns = [
    path("list/", views.RunningCostListView.as_view(), name="running-costs-list")
]
