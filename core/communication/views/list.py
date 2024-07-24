from communication.models import Message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "communication/message-list.html"

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        kwargs["messages_queryset"] = self.get_queryset()
        return super().get_context_data(**kwargs)
