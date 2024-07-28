from accounts.tests import CustomUserFactory
from django.core.management import call_command
from django.test import TestCase, tag
from subscription.models import Subscription
from subscription.tests import PlanFactory, SubscriptionFactory


class CommandTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.plan_1 = PlanFactory.create(price=0)
        self.plan_2 = PlanFactory.create()
        self.subscription = SubscriptionFactory(plan=self.plan_1, user=self.user)
        self.subscription_2 = SubscriptionFactory(plan=self.plan_2, user=self.user)

    @tag("test")
    def test_update_subscription_status_command(self):
        call_command("update_subscription_status")

        subscriptions = Subscription.objects.all()

        self.assertTrue(subscriptions.last().is_active)
        self.assertFalse(subscriptions.first().is_active)
