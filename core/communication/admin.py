from communication.models.messages import Message
from django.contrib import admin


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_filter = ["is_read", "created_at"]
    search_fields = ["user__email", "user__username"]
