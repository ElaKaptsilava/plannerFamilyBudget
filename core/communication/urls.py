from django.urls import path

from .views import MessageListView

app_name = "communication"

urlpatterns = [
    path("", MessageListView.as_view(), name="message-list"),
]
