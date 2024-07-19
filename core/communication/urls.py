from django.urls import path

from .views import MessageListView
from .views.detail import MessageDetailView

app_name = "communication"

urlpatterns = [
    path("", MessageListView.as_view(), name="message-list"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message-detail"),
]
