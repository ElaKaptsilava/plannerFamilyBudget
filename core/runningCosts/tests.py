from accounts.factories import CustomUserFactory
from django.test import TestCase, tag
from django.utils import timezone

from .factories import RunningCostCategoryFactory, RunningCostFactory
from .models import RunningCost


class RunningCostsFilterTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory()
        self.category = RunningCostCategoryFactory.create()
        now = timezone.now()

        self.cost = RunningCostFactory(
            category=self.category, user=self.user, payment_deadline=now
        )
        self.cost1 = RunningCostFactory(
            category=self.category,
            user=self.user,
            payment_deadline=now - timezone.timedelta(days=1),
        )
        self.cost2 = RunningCostFactory(
            category=self.category,
            user=self.user,
            payment_deadline=now + timezone.timedelta(days=1),
        )
        self.cost3 = RunningCostFactory(
            category=self.category,
            user=self.user,
            payment_deadline=now + timezone.timedelta(days=2),
        )

    @tag("x")
    def test_filter(self):
        self.client.force_login(self.user)
        x = RunningCost.objects.all()
        print(x)
        print(x.order_by("-amount"))
        # response = self.client.get(reverse_lazy("running-costs:running-costs-list"), {"sort_by": "-amount"})
        # print(response.context["object_list"])
