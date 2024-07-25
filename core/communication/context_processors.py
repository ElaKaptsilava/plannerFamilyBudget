from communication.models import Message
from django.db.models import QuerySet


def get_unread_messages_context(request) -> dict[str, int | QuerySet[Message]]:
    context = {
        "unread_messages_count": 0,
        "unread_messages": Message.objects.none(),
    }

    if request.user.is_authenticated:
        messages = Message.objects.filter(
            user=request.user, title__startswith="Budget analiz", is_read=False
        )
        context.update(
            {
                "unread_messages_count": messages.count(),
                "unread_messages": messages,
            }
        )

    return context
