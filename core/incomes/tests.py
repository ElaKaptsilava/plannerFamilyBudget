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

    @tag("x")
    def test_logged_user_create_incomes_success(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse_lazy("incomes:create_income"), self.cleaned_data
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Income.objects.filter(user__email=self.user.email).count(), 1)
