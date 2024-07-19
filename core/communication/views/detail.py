from communication.models import Message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "communication/detail.html"
    context_object_name = "message"
    success_message = "Message successfully sent!"
