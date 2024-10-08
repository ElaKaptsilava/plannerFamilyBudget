from django.contrib import admin

from .models import RunningCost, RunningCostCategory


@admin.register(RunningCostCategory)
class RunningCostsCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]
    list_per_page = 20


@admin.register(RunningCost)
class RunningCostAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "category",
        "amount",
        "period_type",
        "period",
        "next_payment_date",
    )
    list_filter = ("user", "category", "period_type", "period", "next_payment_date")
    search_fields = ("user__username", "category__name")
    list_per_page = 20
