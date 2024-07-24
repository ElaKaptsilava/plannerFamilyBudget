from django.urls import path

from .views import MessageDetailView, MessageListView

app_name = "communication"

urlpatterns = [
    path("messages/", MessageListView.as_view(), name="messages-list"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message-detail"),
]
