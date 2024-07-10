from communication.models import Message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    # template_name = 'communication/list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
