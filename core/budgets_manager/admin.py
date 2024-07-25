from django.contrib import admin

from .models import BudgetManager, LimitManager, MonthlyIncomes, WantsManager


@admin.register(LimitManager)
class PlanerAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(BudgetManager)
class BudgetManagerAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(MonthlyIncomes)
class MonthlyIncomesAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(WantsManager)
class WantsManagerAdmin(admin.ModelAdmin):
    list_per_page = 20
