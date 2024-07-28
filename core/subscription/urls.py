from django.urls import path
from subscription.views import CreateSubscriptionView

app_name = "subscription"

urlpatterns = [
    path("choise/", CreateSubscriptionView.as_view(), name="list-create"),
]
