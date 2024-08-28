from accounts.tests import CustomUserFactory
from budgets_manager.tests import BudgetManagerFactory
from django.test import TestCase
from expenses.tests import ExpenseCategoryFactory, ExpenseFactory
from expenses.types import Type
from incomes.tests.factories import IncomeFactory
from runningCosts.tests.factories import RunningCostCategoryFactory, RunningCostFactory


class CommandTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget = BudgetManagerFactory.create(user=self.user)
        self.incomes = IncomeFactory.create_batch(user=self.user, size=3)
        self.expense_category1 = ExpenseCategoryFactory.create(user=self.user)
        self.expense_category2 = ExpenseCategoryFactory.create(
            user=self.user, type=Type.WANTS
        )
        self.expense = ExpenseFactory.create(
            user=self.user, category=self.expense_category1
        )
        self.expense2 = ExpenseFactory.create(
            user=self.user, category=self.expense_category2
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

    # @patch(
    #     "communication.management.commands.open_ai_message.Command.get_openai_response"
    # )
    # def test_command_output(self, mock_get_openai_response):
    #     mock_get_openai_response.return_value = self.mock_open_ai_response()
    #     out = StringIO()
    #
    #     self.client.force_login(self.user)
    #
    #     with patch("sys.stdout", new=out):
    #         call_command("open_ai_message")
    #
    #     captured_output = out.getvalue().strip()
    #     self.assertEqual(captured_output, self.success_message)

    # @patch(
    #     "communication.management.commands.open_ai_message.Command.get_openai_response"
    # )
    # def test_create_budget_message(self, mock_get_openai_response):
    #     mock_get_openai_response.return_value = self.mock_open_ai_response()
    #     mock_now = timezone.now()
    #
    #     with patch("django.utils.timezone.now", return_value=mock_now):
    #         command = Command()
    #         command.create_budget_message()
    #
    #     messages = Message.objects.all()
    #     expected_title = f"Budget analiz {mock_now.strftime('%B')} {mock_now.year}"
    #     self.assertTrue(all(message.title == expected_title for message in messages))
