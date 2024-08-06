from django.contrib import admin
from multi_user.models import Collaboration, CollaborationUser, Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ["email", "token"]
    search_fields = ["email"]


@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    pass


@admin.register(CollaborationUser)
class CollaborationUserAdmin(admin.ModelAdmin):
    list_display = ["user", "collaboration"]
