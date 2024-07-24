from django.urls import path
from subscription.views import CreateSubscriptionView, UpdateSubscriptionView

app_name = "subscription"

urlpatterns = [
    path("choise/", CreateSubscriptionView.as_view(), name="list-create"),
    path("<int:pk>/update/", UpdateSubscriptionView.as_view(), name="detail-update"),
]
