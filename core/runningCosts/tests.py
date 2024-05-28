from accounts.factories import CustomUserFactory
from django.test import TestCase, tag
from django.urls import reverse_lazy
from django.utils import timezone

from .factories import RunningCostCategoryFactory, RunningCostFactory
from .models import RunningCost


class RunningCostsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory()
        self.category = RunningCostCategoryFactory.create()
        now = timezone.now()

        self.cost = RunningCostFactory.create(
            category=self.category, user=self.user, payment_deadline=now
        )
        self.cost_build = RunningCostFactory.build()

    def test_user_add_running_cost_success(self):
        self.client.force_login(self.user)

        data_cleaned = {
            "category": self.category.pk,
            "name": self.cost_build.name,
            "amount": 1234.80,
            "period_type": "months",
            "period": 1,
            "due_date": self.cost_build.due_date,
            "payment_deadline": self.cost_build.payment_deadline,
            "is_paid": self.cost_build.is_paid,
        }

        response = self.client.post(
            reverse_lazy("running-costs:running-costs-list"), data_cleaned
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(RunningCost.objects.all().count(), 2)
        self.assertTrue(RunningCost.objects.get(name=self.cost_build.name))
        self.assertEqual(
            RunningCost.objects.get(name=self.cost_build.name).user, self.user
        )

    @tag("x")
    def test_user_add_running_cost_with_invalid_data_failed(self):
        self.client.force_login(self.user)

        invalid_data = {}

        response = self.client.post(
            reverse_lazy("running-costs:running-costs-list"), invalid_data
        )

        print(response)
