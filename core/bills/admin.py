from django.contrib import admin

from . import models


@admin.register(models.Bill)
class BillAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
