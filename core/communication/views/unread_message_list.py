from communication.models.messages import Message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class UnreadMessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "communication/unread-messages.html"
    context_object_name = "unread_messages"

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user, title__startswith="Budget analiz", is_read=False
        )

    def get_context_data(self, **kwargs):
        kwargs["unread_messages"] = self.get_queryset()
        return super().get_context_data(**kwargs)
