from accounts.tests import CustomUserFactory
from budgets_manager.tests.factories.budget_manager_factory import BudgetManagerFactory
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from incomes.models import Income
from incomes.tests.factories import IncomeFactory
from rest_framework import status


class IncomesTests(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget = BudgetManagerFactory.create(user=self.user)
        self.income = IncomeFactory.build(user=self.user, budget=self.budget)
        self.cleaned_data = {
            "source": self.income.source,
            "category": self.income.category,
            "amount": self.income.amount,
            "date": self.income.date,
        }

    def test_logged_user_create_incomes_success(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse_lazy("incomes:incomes-list"), self.cleaned_data
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Income.objects.count(), 1)

    def test_user_get_incomes_success(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse_lazy("incomes:incomes-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Income.objects.filter(user__email=self.user.email).count(), 0)

    def test_update_incomes_success(self):
        self.client.force_login(self.user)

        income = IncomeFactory.create(user=self.user, budget=self.budget)

        response = self.client.post(
            reverse_lazy("incomes:incomes-detail-update", kwargs={"pk": income.pk}),
            self.cleaned_data,
        )

        income_get = Income.objects.get(pk=income.pk)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(income_get.source, self.cleaned_data["source"])
        self.assertEqual(income_get.amount, self.cleaned_data["amount"])


class DeleteIncomesTests(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget = BudgetManagerFactory.create(user=self.user)
        self.income = IncomeFactory.build(user=self.user, budget=self.budget)
        self.cleaned_data = {
            "source": self.income.source,
            "category": self.income.category,
            "amount": self.income.amount,
            "date": self.income.date,
        }

    def test_user_delete_incomes_success(self):
        self.client.force_login(self.user)

        self.client.post(reverse_lazy("incomes:incomes-list"), self.cleaned_data)

        income = Income.objects.first()
        initial_incomes_count = Income.objects.count()

        self.assertEqual(initial_incomes_count, 1)

        response = self.client.post(
            reverse("incomes:incomes-delete-multiple"),
            data={"selected_incomes": [income.id]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Income.objects.count(), initial_incomes_count - 1)

    def test_user_delete_incomes_no_selection(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("incomes:incomes-delete-multiple"), {"selected_incomes": []}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("incomes:incomes-list"))
