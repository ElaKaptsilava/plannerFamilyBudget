from django.contrib import admin
from subscription.models import CreditCard, Payment, Plan, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_filter = ["end_date"]
    search_fields = ["user__username", "user__email", "end_date"]
    list_display = ["user", "plan", "start_date", "end_date", "is_active"]


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ["name", "price"]


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ["owner__username", "owner__email"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_filter = ["amount", "date"]
