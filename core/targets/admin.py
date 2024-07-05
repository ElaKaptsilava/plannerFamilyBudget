from django.contrib import admin

from .models import Saving, SavingContributions, Target, TargetContribution


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    pass


@admin.register(TargetContribution)
class TargetContributionAdmin(admin.ModelAdmin):
    pass


@admin.register(SavingContributions)
class SavingContributionsAdmin(admin.ModelAdmin):
    pass


@admin.register(Saving)
class SavingAdmin(admin.ModelAdmin):
    pass
