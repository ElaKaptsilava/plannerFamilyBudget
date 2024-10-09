from accounts.tests import CustomUserFactory
from django.test import TestCase
from django.utils import timezone
from targets.tests.factories import TargetContributionFactory, TargetFactory

from core.constants import labels


class TargetModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.target = TargetFactory.create(user=self.user, amount=1000)

    def test_create_target(self):
        """Test the creation of a Target instance."""
        self.assertEqual(self.target.user, self.user)
        self.assertEqual(self.target.amount, 1000.0)
        self.assertIsInstance(self.target.deadline, timezone.datetime)

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

    def test_monthly_payment(self):
        deadline = timezone.now() + timezone.timedelta(days=62)
        target = TargetFactory.create(user=self.user, deadline=deadline.date())

        expected_amount = target.amount / 2

        self.assertEqual(target.monthly_payment, expected_amount)

    def test_completed_status_label(self):
        """Test the completed_status_label property."""
        self.target.targetcontribution_set.create(amount=900.0, user=self.user)
        self.assertEqual(self.target.completed_status_label, labels.WARNING)

        self.target.targetcontribution_set.create(amount=100.0, user=self.user)
        self.assertEqual(self.target.completed_status_label, labels.SUCCESS)

    def test_update_deadline(self):
        """Test the update_deadline method."""
        original_deadline = self.target.deadline
        self.target.update_deadline()
        self.assertEqual(
            self.target.deadline, original_deadline + timezone.timedelta(days=30)
        )
