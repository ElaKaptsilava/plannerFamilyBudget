from django.contrib import admin
from multi_user.models import FamilyBudget, InvitationToken


@admin.register(InvitationToken)
class InvitationTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(FamilyBudget)
class FamilyBudgetAdmin(admin.ModelAdmin):
    pass
