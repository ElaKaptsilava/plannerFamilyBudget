from communication.models.messages import Message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "communication/alert_messages.html"
    context_object_name = "messages"

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user, title__startswith="Budget analiz"
        )

    def get_context_data(self, **kwargs):
        kwargs["alert_messages"] = self.get_queryset()
        return super().get_context_data(**kwargs)
