from django.contrib import admin

from .models import BudgetManager, Planer


@admin.register(Planer)
class PlanerAdmin(admin.ModelAdmin):
    pass


@admin.register(BudgetManager)
class BudgetManagerAdmin(admin.ModelAdmin):
    pass
