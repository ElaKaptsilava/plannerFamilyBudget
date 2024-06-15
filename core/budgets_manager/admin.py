from django.contrib import admin

from .models import BudgetManager, LimitManager


@admin.register(LimitManager)
class PlanerAdmin(admin.ModelAdmin):
    pass


@admin.register(BudgetManager)
class BudgetManagerAdmin(admin.ModelAdmin):
    pass
