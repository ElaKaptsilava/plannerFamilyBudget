import datetime

from accounts.tests import CustomUserFactory
from budgets_manager.tests.factories.budget_manager_factory import BudgetManagerFactory
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy
from runningCosts.models import RunningCost
from runningCosts.tests.factories import RunningCostCategoryFactory, RunningCostFactory


class RunningCostsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget = BudgetManagerFactory.create(user=self.user)
        self.category = RunningCostCategoryFactory.create(user=self.user)
        self.cost_build = RunningCostFactory.build(
            category=self.category,
            next_payment_date=datetime.date(3024, 1, 1),
            payment_deadline=datetime.date(3025, 1, 1),
        )

        self.cost_cleaned_data = {
            "category": self.category.pk,
            "next_payment_date": self.cost_build.next_payment_date,
            "payment_deadline": self.cost_build.payment_deadline,
            "period": self.cost_build.period,
            "period_type": self.cost_build.period_type,
            "amount": self.cost_build.amount,
            "name": self.cost_build.name,
        }

    def test_user_create_cost_success(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse_lazy("running-costs:running-costs-list"),
            data=self.cost_cleaned_data,
        )

        messages = list(get_messages(response.wsgi_request))
        cost = RunningCost.objects.all().first()

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "The running cost added successfully!")
        self.assertTrue(cost)
        self.assertFalse(cost.is_paid)
        self.assertFalse(cost.has_overdue)
        self.assertFalse(cost.is_completed)

    def test_user_create_cost_failure(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse_lazy("running-costs:running-costs-list"), data={}
        )

        messages = list(get_messages(response.wsgi_request))
        costs = RunningCost.objects.all()

        self.assertEqual(len(messages), 1)
        self.assertEqual(
            messages[0].message,
            "Failed to add the running cost. Please check the form.",
        )
        self.assertFalse(costs)

    def test_user_delete_costs_success(self):
        self.client.force_login(self.user)

        cost = RunningCostFactory.create(user=self.user, category=self.category)
        cost1 = RunningCostFactory.create(user=self.user, category=self.category)
        cost2 = RunningCostFactory.create(user=self.user, category=self.category)
        cost3 = RunningCostFactory.create(user=self.user, category=self.category)

        self.assertEqual(RunningCost.objects.all().count(), 4)

        selected_costs = [cost.pk, cost1.pk, cost2.pk]

        response = self.client.post(
            reverse_lazy("running-costs:running-costs-list-delete-multiple"),
            data={"selected_costs": selected_costs},
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, 25)
        self.assertEqual(RunningCost.objects.all().count(), 1)
        self.assertTrue(RunningCost.objects.get(pk=cost3.pk))

    def test_user_delete_costs_failure(self):
        self.client.force_login(self.user)

        cost = RunningCostFactory.create(user=self.user, category=self.category)

        selected_costs = []

        response = self.client.post(
            reverse_lazy("running-costs:running-costs-list-delete-multiple"),
            data={"selected_costs": selected_costs},
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, 40)
        self.assertEqual(RunningCost.objects.all().count(), 1)
        self.assertTrue(RunningCost.objects.filter(pk=cost.pk).exists())

    def test_user_update_costs_success(self):
        self.client.force_login(self.user)

        cost = RunningCostFactory.create(user=self.user, category=self.category)

        response = self.client.post(
            reverse_lazy(
                "running-costs:running-costs-detail-update", kwargs={"pk": cost.pk}
            ),
            data=self.cost_cleaned_data,
        )

        messages = list(get_messages(response.wsgi_request))
        get_cost = RunningCost.objects.get(pk=cost.pk)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, 25)
        self.assertEqual(get_cost.amount, self.cost_cleaned_data["amount"])
        self.assertEqual(
            get_cost.payment_deadline, self.cost_cleaned_data["payment_deadline"]
        )

    def test_user_update_costs_failure(self):
        self.client.force_login(self.user)

        cost = RunningCostFactory.create(user=self.user, category=self.category)

        response = self.client.post(
            reverse_lazy(
                "running-costs:running-costs-detail-update", kwargs={"pk": cost.pk}
            ),
            data={},
        )

        messages = list(get_messages(response.wsgi_request))
        get_cost = RunningCost.objects.get(pk=cost.pk)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, 40)
        self.assertEqual(RunningCost.objects.all().count(), 1)
        self.assertEqual(get_cost.amount, cost.amount)
        self.assertEqual(get_cost.payment_deadline, cost.payment_deadline.date())
