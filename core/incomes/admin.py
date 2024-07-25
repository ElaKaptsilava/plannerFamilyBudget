from django.contrib import admin

from .models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ["category"]
    list_filter = ["user__email"]
