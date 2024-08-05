from django.contrib import admin
from multi_user.models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ["budget", "email", "token"]
    search_fields = ["budget", "email"]
