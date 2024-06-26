from accounts.factories import CustomUserFactory
from django.test import TestCase, tag
from django.urls import reverse, reverse_lazy
from rest_framework import status

from .factories import IncomeFactory
from .models import Income


class IncomesTests(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.income = IncomeFactory.build(user=self.user)
        self.cleaned_data = {
            "source": self.income.source,
            "category": self.income.category,
            "amount": self.income.amount,
            "date": self.income.date,
        }

    def test_logged_user_create_incomes_success(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse_lazy("incomes:income-list-create"), self.cleaned_data
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Income.objects.filter(user__email=self.user.email).count(), 1)

    def test_user_get_incomes_success(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse_lazy("incomes:incomes-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Income.objects.filter(user__email=self.user.email).count(), 0)

    def test_update_incomes_success(self):
        self.client.force_login(self.user)

        income = IncomeFactory.create(user=self.user)

        response = self.client.post(
            reverse_lazy("incomes:income-detail-update", kwargs={"pk": income.pk}),
            self.cleaned_data,
        )

        income_get = Income.objects.get(pk=income.pk)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(income_get.source, self.cleaned_data["source"])
        self.assertEqual(income_get.amount, self.cleaned_data["amount"])


class DeleteIncomesTests(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.income = IncomeFactory.build(user=self.user)
        self.cleaned_data = {
            "source": self.income.source,
            "category": self.income.category,
            "amount": self.income.amount,
            "date": self.income.date,
        }

    def test_user_delete_incomes_success(self):
        self.client.force_login(self.user)

        self.client.post(reverse_lazy("incomes:income-list-create"), self.cleaned_data)

        income = Income.objects.get(user__email=self.user.email)
        initial_incomes_count = Income.objects.count()

        self.assertEqual(initial_incomes_count, 1)

        response = self.client.post(
            reverse("incomes:delete-multiple"), {"selected_incomes": [income.id]}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Income.objects.count(), initial_incomes_count - 1)

    @tag("x")
    def test_user_delete_incomes_no_selection(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("incomes:delete-multiple"), {"selected_incomes": []}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("incomes:incomes-list"))
