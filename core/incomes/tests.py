from accounts.factories import CustomUserFactory
from django.test import TestCase, tag
from django.urls import reverse_lazy
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
            reverse_lazy("incomes:create_income"), self.cleaned_data
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Income.objects.filter(user__email=self.user.email).count(), 1)

    def test_user_get_incomes_success(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse_lazy("incomes:incomes"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Income.objects.filter(user__email=self.user.email).count(), 0)

    @tag("x")
    def test_user_delete_incomes_success(self):
        self.client.force_login(self.user)

        IncomeFactory.create(user=self.user)
        income2 = IncomeFactory.create(user=self.user)

        response = self.client.delete(
            reverse_lazy("incomes:income_delete", kwargs={"income_pk": income2.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Income.objects.filter(user__email=self.user.email).count(), 1)
