from django.contrib import admin

from .models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    pass
