from accounts.models import CustomUser
from budgets_manager.constants import TODAY
from budgets_manager.models import BudgetManager, NeedsManager, WantsManager
from communication.models import Message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from targets.forms import (
    SavingNegativeContributionsForm,
    SavingPositiveContributionsForm,
)
from targets.models import Saving


class DropMenuView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "index.html"

    def get_alert_messages_queryset(self) -> QuerySet[Message]:
        return Message.objects.filter(
            user=self.request.user,
            title__startswith="Budget analiz",
            created_at__month=TODAY.month,
        )

    def count_unread_alert_messages(self) -> QuerySet[Message]:
        return self.get_alert_messages_queryset().filter(is_read=False).count()

    def get_context_data(self, **kwargs):
        kwargs["alert_messages"] = self.get_alert_messages_queryset()
        kwargs["unread_alert_count"] = self.count_unread_alert_messages()
        return super().get_context_data(**kwargs)


class HomeView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name: str = "accounts/dashboard.html"
    http_method_names: list = ["get"]

    def get_context_data(self, **kwargs):
        kwargs["budget"] = self.get_budget_object()
        kwargs["needs"] = self.get_needs_manager_object_or_404()
        kwargs["wants"] = self.get_wants_manager_object_or_404()
        kwargs["savings"] = self.get_savings_object_or_404()
        kwargs["positive_form"] = SavingPositiveContributionsForm()
        kwargs["negative_form"] = SavingNegativeContributionsForm()
        kwargs["alert_messages"] = self.get_alert_messages_queryset()
        kwargs["unread_alert_count"] = self.count_unread_alert_messages()
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def get_alert_messages_queryset(self) -> QuerySet[Message]:
        return Message.objects.filter(
            user=self.request.user,
            title__startswith="Budget analiz",
            created_at__month=TODAY.month,
        )

    def count_unread_alert_messages(self) -> QuerySet[Message]:
        return self.get_alert_messages_queryset().filter(is_read=False).count()

    def get_budget_object(self) -> QuerySet[BudgetManager]:
        return self.request.user.budgetmanager

    def get_needs_manager_object_or_404(self) -> QuerySet[NeedsManager]:
        return get_object_or_404(
            NeedsManager.objects.select_related("user"), user=self.request.user
        )

    def get_wants_manager_object_or_404(self) -> QuerySet[WantsManager]:
        return get_object_or_404(
            WantsManager.objects.select_related("user"), user=self.request.user
        )

    def get_savings_object_or_404(self) -> QuerySet[Saving]:
        return get_object_or_404(
            Saving.objects.select_related("user"), user=self.request.user
        )
