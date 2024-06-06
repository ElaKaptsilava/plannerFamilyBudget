import datetime

from accounts.factories import CustomUserFactory
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils import timezone

from .factories import RunningCostCategoryFactory, RunningCostFactory
from .models import RunningCost


class RunningCostsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory()
        self.category = RunningCostCategoryFactory.create()
        self.now = timezone.now().date()

        self.cost = RunningCostFactory.create(
            category=self.category,
            user=self.user,
            payment_deadline=self.now,
            period_type="months",
            period=1,
            next_payment_date=timezone.now().date(),
        )
        self.cost_build = RunningCostFactory.build()
        self.data_cleaned = {
            "category": self.category.pk,
            "name": self.cost_build.name,
            "amount": 1234.80,
            "period_type": "months",
            "period": 1,
            "next_payment_date": timezone.now().date(),
            "payment_deadline": self.now + timezone.timedelta(days=700),
            "is_paid": self.cost_build.is_paid,
        }

    def test_user_add_running_cost_success(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse_lazy("running-costs:running-costs-list"), self.data_cleaned
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(RunningCost.objects.all().count(), 2)
        self.assertTrue(RunningCost.objects.get(name=self.cost_build.name))
        self.assertEqual(
            RunningCost.objects.get(name=self.cost_build.name).user, self.user
        )

    def test_cost_is_completed(self):
        self.client.force_login(self.user)

        self.cost.is_paid = True
        self.cost.save()

        self.assertTrue(self.cost.is_completed)

    def test_change_next_payment_date_month_period(self):
        self.client.force_login(self.user)

        self.data_cleaned.update(
            {
                "next_payment_date": datetime.date(2024, 5, 31),
                "period_type": "months",
                "period": 2,
            }
        )
        response = self.client.post(
            reverse_lazy("running-costs:running-costs-list"), self.data_cleaned
        )

        self.assertEqual(response.status_code, 302)

        cost = RunningCost.objects.get(name=self.data_cleaned["name"])
        cost.is_paid = True
        cost.save()

        required_date = datetime.date(2024, 7, 31)

        self.assertEqual(cost.next_payment_date, required_date)

    def test_change_next_payment_date_year_period(self):
        self.client.force_login(self.user)

        self.data_cleaned.update(
            {
                "next_payment_date": datetime.date(2024, 5, 31),
                "period_type": "years",
                "period": 1,
            }
        )
        response = self.client.post(
            reverse_lazy("running-costs:running-costs-list"), self.data_cleaned
        )

        self.assertEqual(response.status_code, 302)

        cost = RunningCost.objects.get(name=self.data_cleaned["name"])
        cost.is_paid = True
        cost.save()

        required_date = datetime.date(2025, 8, 31)

        self.assertEqual(cost.next_payment_date, required_date)
