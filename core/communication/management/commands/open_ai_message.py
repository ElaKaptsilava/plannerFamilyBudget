from typing import Any, Optional

from accounts.models import CustomUser
from budgets_manager.models import NeedsManager, WantsManager
from communication.models.messages import Message
from django.core.management.base import BaseCommand
from django.db.models import QuerySet, Sum
from django.utils import timezone
from openai import OpenAI
from openai.types.chat import ChatCompletion
from subscription.models import Plan


class Command(BaseCommand):
    help = (
        "Create a message for the current user with their budget status using OpenAI."
    )

    def handle(self, *args: Any, **options: Any) -> None:
        self.create_budget_message()

        self.stdout.write(
            self.style.SUCCESS("Successfully created alert messages with openai.")
        )

    def create_budget_message(self) -> None:
        users: QuerySet[CustomUser] = CustomUser.objects.select_related(
            "set_budget__budget"
        ).prefetch_related("expense_categories")
        basic_plan_names = set(
            Plan.objects.filter(price=0).values_list("name", flat=True)
        )
        for user in users:
            user_plan = user.subscription_set.last().plan
            if user_plan.name in basic_plan_names:
                continue
            needs_manager: NeedsManager = NeedsManager.objects.get(user=user)
            wants_manager: WantsManager = WantsManager.objects.get(user=user)

            summary: str = self.write_summary(
                user=user, needs_manager=needs_manager, wants_manager=wants_manager
            )

            prompt: str = (
                f"Generate a message for the user about their budget status with the following information:\n{summary}\n"
            )
            message_content: str = self.get_openai_response(
                user=user.username, prompt=prompt
            )

            current_day = timezone.now().strftime("%d")
            current_month = timezone.now().strftime("%B")
            current_year = timezone.now().year

            message: Message = Message(
                user=user,
                title=f"Budget analiz {current_day} {current_month} {current_year} for {user.username}",
                content=message_content,
                created_at=timezone.now(),
                is_read=False,
            )
            message.save()

    @staticmethod
    def get_system_content_from_file() -> str:
        with open("communication/management/commands/content.txt", "r") as content_file:
            return content_file.read()

    def get_openai_response(self, user: str, prompt: str) -> str:
        client = OpenAI()
        content = self.get_system_content_from_file().replace("user", f"{user}'s")
        completion: ChatCompletion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": content},
                {"role": "user", "content": prompt},
            ],
        )

        return completion.choices[0].message.content.replace("[Your Name]", "")

    @staticmethod
    def calculate_savings_monthly(user: CustomUser, budget: Any) -> float:
        savings_monthly: QuerySet = user.saving.savingcontributions_set.filter(
            date__range=budget.get_month_range()
        )
        total: Optional[float] = savings_monthly.aggregate(total_sav=Sum("amount"))[
            "total_sav"
        ]
        return total or 0.0

    def write_summary(
        self, user: CustomUser, wants_manager: WantsManager, needs_manager: NeedsManager
    ) -> str:
        budget: Any = user.set_budget.budget
        wants_expenses = WantsManager.objects.get(user=user)
        needs = NeedsManager.objects.get(user=user)
        summary: str = (
            f"User: {user.username}\n\n"
            f"Monthly Budget Plan:\n"
            f"For wants: {budget.wants_percentage}%\n"
            f"Wants budget progress: {wants_manager.get_progress}\n"
            f"Is within wants limit: {wants_manager.is_within_wants_budget}\n\n"
            f"For needs: {budget.needs_percentage}%\n"
            f"Needs budget progress: {needs_manager.get_progress}\n"
            f"Is within needs limit: {needs_manager.is_within_needs_budget}\n\n"
            f"For savings: {budget.savings_percentage}%\n"
            f"Total savings (monthly): {self.calculate_savings_monthly(user=user, budget=budget)}\n"
            f"Total savings: {user.saving.total_amount}\n\n"
            f"Total monthly incomes: {budget.total_monthly_incomes}\n"
            f"Total monthly expenses: {budget.total_monthly_expenses}\n"
            f"Total want expenses (monthly): {wants_expenses.total_monthly_wants_expenses}\n"
            f"Total need expenses (monthly): {needs.total_monthly_needs_expenses}\n"
            f"Total running costs: {needs_manager.total_costs_spent_in_month}\n"
        )
        last_message = user.messages.first()
        if last_message:
            summary += f"last your proposed message: {last_message.content}\n"
        return summary
