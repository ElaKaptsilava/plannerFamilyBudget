from accounts.tests import CustomUserFactory
from budgets_manager.tests.factories.budget_manager_factory import BudgetManagerFactory
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy
from expenses.tests.factories import ExpenseCategoryFactory


class CategoryListViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.user2 = CustomUserFactory.create()

        self.budget = BudgetManagerFactory.create(user=self.user)
        self.budget2 = BudgetManagerFactory.create(user=self.user2)

        self.category_create1 = ExpenseCategoryFactory.create(user=self.user)
        self.category_create2 = ExpenseCategoryFactory.create(user=self.user)

        self.url_list = reverse_lazy("expenses:category-list")

        self.level_info = 20

    def test_get_category_list_success(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, 200)

    def test_get_category_list_when_not_expenses(self):
        self.client.force_login(self.user2)

        response = self.client.get(self.url_list)

        message = list(get_messages(response.wsgi_request))[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(message.level, self.level_info)
