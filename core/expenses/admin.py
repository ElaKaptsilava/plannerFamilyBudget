from django.contrib import admin
from expenses.models import Expense, ExpenseCategory


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_filter = ["category__name", "datetime"]
    search_fields = ["user__email", "user__username"]


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ["name"]
    list_filter = ["user__username", "user__email"]
