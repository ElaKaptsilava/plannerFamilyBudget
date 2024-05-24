from django.contrib import admin

from .models import RunningCost, RunningCostCategory


@admin.register(RunningCostCategory)
class RunningCostsCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(RunningCost)
class RunningCostAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "amount", "period_type", "period", "due_date")
    list_filter = ("user", "category", "period_type", "period", "due_date")
    search_fields = ("user__username", "category__name")
