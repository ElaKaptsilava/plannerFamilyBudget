from io import StringIO
from unittest.mock import patch

from accounts.tests import CustomUserFactory
from budgets_manager.tests.factories.budget_manager_factory import BudgetManagerFactory
from communication.management.commands.open_ai_message import Command
from communication.models import Message
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from expenses.tests.factories import ExpenseCategoryFactory, ExpenseFactory
from incomes.tests.factories import IncomeFactory
from runningCosts.tests.factories import RunningCostCategoryFactory, RunningCostFactory
from subscription.models import Status
from subscription.tests.factories import PlanFactory, SubscriptionFactory


class CommandTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget = BudgetManagerFactory.create(user=self.user)

        self.plan = PlanFactory(price=100)
        self.subscription = SubscriptionFactory.create(user=self.user, plan=self.plan)
        self.subscription.payment.status = Status.COMPLETED
        self.subscription.save()

        self.incomes = IncomeFactory.create_batch(
            user=self.user, budget=self.budget, size=3
        )
        self.expense_category = ExpenseCategoryFactory.create(user=self.user)
        self.expense = ExpenseFactory.create(
            user=self.user, category=self.expense_category, budget=self.budget
        )
        self.category_cost = RunningCostCategoryFactory.create(user=self.user)
        self.running_cost = RunningCostFactory.create(
            user=self.user, category=self.category_cost
        )

        self.success_message = "Successfully created alert messages with openai."

    @staticmethod
    def mock_open_ai_response():
        with open("communication/tests/open_ai_output.txt") as response:
            return response.read()

    @patch(
        "communication.management.commands.open_ai_message.Command.get_openai_response"
    )
    def test_command_output(self, mock_get_openai_response):
        mock_get_openai_response.return_value = self.mock_open_ai_response()
        out = StringIO()
        self.client.force_login(self.user)
        with patch("sys.stdout", new=out):
            call_command("open_ai_message")
        #
        captured_output = out.getvalue().strip()
        print(captured_output)
        self.assertEqual(captured_output, self.success_message)

    @patch(
        "communication.management.commands.open_ai_message.Command.get_openai_response"
    )
    def test_create_budget_message(self, mock_get_openai_response):
        mock_get_openai_response.return_value = self.mock_open_ai_response()
        mock_now = timezone.now()

        with patch("django.utils.timezone.now", return_value=mock_now):
            command = Command()
            command.create_budget_message()

        message = Message.objects.first()

        date_str = f"{message.created_at.strftime('%d')} {message.created_at.strftime('%B')} {message.created_at.strftime('%Y')}"
        expected_title = f"Budget analiz {date_str} for {message.user.username}"

        self.assertTrue(message.title == expected_title)
