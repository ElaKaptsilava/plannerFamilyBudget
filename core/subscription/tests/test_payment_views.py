from accounts.tests import CustomUserFactory
from budgets_manager.tests import BudgetManagerFactory
from django.test import TestCase
from django.urls import reverse_lazy
from subscription.tests import PlanFactory


class PaymentViewTest(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget = BudgetManagerFactory.create(user=self.user)
        self.plan_1 = PlanFactory.create()
        self.plan_2 = PlanFactory.create(price=0)
        self.create_subscription_url = reverse_lazy("subscription:list-create")

    @staticmethod
    def payment_path(payment_id):
        return reverse_lazy("payment", kwargs={"payment_id": payment_id})

    def test_user_choice_subscription_with_plan_price_greate_than_0(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.create_subscription_url, data={"plan": self.plan_1.pk}
        )

        self.assertRedirects(response, self.payment_path(payment_id=self.plan_1.pk))

    def test_user_choice_subscription_with_plan_price_0(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.create_subscription_url, data={"plan": self.plan_2.pk}
        )

        self.assertRedirects(response, reverse_lazy("home"))
