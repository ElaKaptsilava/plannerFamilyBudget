from django.contrib import admin

from .models import BudgetManager, LimitManager, MonthlyIncomes, WantsManager


@admin.register(LimitManager)
class PlanerAdmin(admin.ModelAdmin):
    pass


@admin.register(BudgetManager)
class BudgetManagerAdmin(admin.ModelAdmin):
    pass


@admin.register(MonthlyIncomes)
class MonthlyIncomesAdmin(admin.ModelAdmin):
    pass


@admin.register(WantsManager)
class WantsManagerAdmin(admin.ModelAdmin):
    pass
