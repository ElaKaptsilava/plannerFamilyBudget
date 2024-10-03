# from accounts.tests import CustomUserFactory
# from dateutil.relativedelta import relativedelta
# from django.test import TestCase
# from django.utils import timezone
#
# from ..models import Status
# from . import PlanFactory, SubscriptionFactory
#
#
# class SubscriptionModalTestCase(TestCase):
#     def setUp(self):
#         self.user = CustomUserFactory.create()
#         self.plan_1 = PlanFactory.create()
#         self.plan_2 = PlanFactory.create()
#
#     def test_add_payment_after_subscription_created(self):
#         subscription = SubscriptionFactory.create(user=self.user, plan=self.plan_1)
#         self.assertTrue(subscription.payment)
#         self.assertEqual(subscription.payment.status, Status.PENDING)
#
#     def test_save_sets_start_and_end_dates(self):
#         subscription = SubscriptionFactory.create(user=self.user, plan=self.plan_1)
#         self.assertEqual(subscription.start_date, timezone.now().date())
#
#         subscription_2 = SubscriptionFactory.create(user=self.user, plan=self.plan_2)
#
#         start_date = subscription.end_date + relativedelta(days=1)
#         end_date = subscription_2.start_date + relativedelta(months=1)
#
#         self.assertEqual(subscription_2.start_date, start_date)
#         self.assertEqual(subscription_2.end_date, end_date)
