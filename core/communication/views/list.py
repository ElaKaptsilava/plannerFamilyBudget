from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView

from ..models import Message


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "communication/message-list.html"
    context_object_name = "messages_queryset"

    def get_queryset(self) -> QuerySet[Message]:
        return Message.objects.filter(user=self.request.user)
