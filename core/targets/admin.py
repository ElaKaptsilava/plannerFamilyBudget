from django.contrib import admin

from .models import Target, TargetContribution


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    pass


@admin.register(TargetContribution)
class TargetContributionAdmin(admin.ModelAdmin):
    pass
