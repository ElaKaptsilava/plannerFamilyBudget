from communication.models.messages import Message
from django.contrib import admin


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
