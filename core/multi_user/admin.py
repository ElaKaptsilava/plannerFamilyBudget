from django.contrib import admin
from multi_user.models import InvitationToken


@admin.register(InvitationToken)
class InvitationTokenAdmin(admin.ModelAdmin):
    pass
