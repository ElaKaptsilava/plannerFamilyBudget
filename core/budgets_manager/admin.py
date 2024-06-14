from django.contrib import admin

from .models import BudgetManager, PlannerManager


@admin.register(PlannerManager)
class PlanerAdmin(admin.ModelAdmin):
    pass


@admin.register(BudgetManager)
class BudgetManagerAdmin(admin.ModelAdmin):
    pass
