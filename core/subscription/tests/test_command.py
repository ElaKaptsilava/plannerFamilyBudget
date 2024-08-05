from accounts.tests import CustomUserFactory
from dateutil.relativedelta import relativedelta
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from subscription.models import Subscription
from subscription.tests import PlanFactory, SubscriptionFactory


class UpdateSubscriptionStatusTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.plan_1 = PlanFactory.create(price=0)
        self.plan_2 = PlanFactory.create()
        self.subscription = SubscriptionFactory(plan=self.plan_1, user=self.user)
        self.subscription_2 = SubscriptionFactory(plan=self.plan_2, user=self.user)

    def test_update_subscription_status_command(self):
        call_command("update_subscription_status")

        subscriptions = Subscription.objects.all()

        self.assertTrue(subscriptions.last().is_active)
        self.assertFalse(subscriptions.first().is_active)


class GenerateSubscriptionStatusTestCase(TestCase):
    def setUp(self):
        self.today = timezone.now()
        self.start_date = timezone.now() - relativedelta(months=1)
        self.user = CustomUserFactory.create()
        self.plan_1 = PlanFactory.create(price=0)

    def test_generate_next_subscription_command_success(self):
        SubscriptionFactory(
            plan=self.plan_1,
            user=self.user,
            start_date=self.start_date,
            end_date=self.today,
            is_active=True,
        )
        subscriptions = Subscription.objects.all()

        self.assertEqual(subscriptions.count(), 1)

        call_command("generate_next_subscription")

        last_subscription = subscriptions.latest("end_date")

        self.assertEqual(subscriptions.count(), 2)
        self.assertFalse(last_subscription.is_active)
        self.assertTrue(hasattr(last_subscription, "payment"))

    def test_generate_next_subscription_command_failure(self):
        subscription = SubscriptionFactory(
            plan=self.plan_1,
            user=self.user,
            start_date=self.start_date,
            end_date=self.today,
        )
        subscriptions = Subscription.objects.all()

        call_command("generate_next_subscription")

        last_subscription = subscriptions.latest("end_date")

        self.assertEqual(subscriptions.count(), 1)
        self.assertEqual(subscription, last_subscription)
