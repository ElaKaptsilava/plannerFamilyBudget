from accounts.factories import CustomUserFactory
from django.test import TestCase, tag
from django.utils import timezone
from targets.tests.factories import TargetContributionFactory, TargetFactory


class TargetModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.target = TargetFactory.create(user=self.user)

    def test_target_is_completed(self):
        TargetContributionFactory.create(
            user=self.user, target=self.target, amount=self.target.amount + 1
        )
        self.assertTrue(self.target.is_completed)

    def test_calculate_total_contributions(self):
        contribution = TargetContributionFactory.create(
            user=self.user, target=self.target
        )
        contribution_1 = TargetContributionFactory.create(
            user=self.user, target=self.target
        )
        contribution_2 = TargetContributionFactory.create(
            user=self.user, target=self.target
        )

        expected_amount = (
            contribution_1.amount + contribution_2.amount + contribution.amount
        )

        self.assertEqual(self.target.total_contributions, expected_amount)

    @tag("test")
    def test_monthly_payment(self):
        deadline = timezone.now() + timezone.timedelta(days=62)
        target = TargetFactory.create(user=self.user, deadline=deadline.date())

        expected_amount = target.amount / 2

        self.assertEqual(target.monthly_payment, expected_amount)
