import datetime

from accounts.tests import CustomUserFactory
from django.test import TestCase
from runningCosts.models import RunningCost
from runningCosts.tests.factories import RunningCostCategoryFactory, RunningCostFactory


class TestNextPaymentDateUpdate(TestCase):

    def setUp(self):
        self.user = CustomUserFactory.create()
        self.category = RunningCostCategoryFactory.create(user=self.user)

    def test_next_payment_date_is_updated_correctly_when_paid_and_period_is_month(self):
        current_payment_date = datetime.date(3024, 1, 1)
        cost = RunningCostFactory.create(
            user=self.user,
            category=self.category,
            next_payment_date=current_payment_date,
            payment_deadline=datetime.date(3025, 1, 1),
            period_type="months",
        )

        self.assertEqual(RunningCost.objects.all().count(), 1)
        self.assertEqual(
            RunningCost.objects.get(pk=cost.pk).next_payment_date, current_payment_date
        )

        cost.is_paid = True
        cost.save()

        expected_next_payment_date = datetime.date(3024, 2, 1)

        self.assertEqual(cost.next_payment_date, expected_next_payment_date)

    def test_is_completed_is_true_when_next_payment_date_lasThen_deadline(self):
        current_payment_date = datetime.date(3024, 1, 2)
        cost = RunningCostFactory.create(
            user=self.user,
            category=self.category,
            next_payment_date=current_payment_date,
            payment_deadline=datetime.date(3025, 1, 1),
            period_type="years",
        )
        self.assertFalse(cost.is_completed)

        cost.is_paid = True
        cost.save()

        self.assertTrue(cost.is_completed)

    def test_next_payment_date_is_updated_correctly_when_year_is_leap_and_paid_and_period_is_years(
        self,
    ):
        current_payment_date = datetime.date(2024, 2, 29)
        deadline = datetime.date(2030, 3, 1)

        cost = RunningCostFactory.create(
            user=self.user,
            category=self.category,
            next_payment_date=current_payment_date,
            payment_deadline=deadline,
            period_type="years",
        )

        cost.is_paid = True
        cost.save()

        expected_next_payment_date = datetime.date(2025, 2, 28)
        self.assertEqual(cost.next_payment_date, expected_next_payment_date)
