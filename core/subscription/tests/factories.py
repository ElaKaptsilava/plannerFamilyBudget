import factory
from accounts.tests import CustomUserFactory

from ..models import Payment, Plan, Status, Subscription


class PlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plan

    name = factory.Sequence(lambda n: f"plan {n}")
    price = factory.Faker("random_int")
    description = factory.Faker("text")


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    user = factory.SubFactory(CustomUserFactory)
    plan = factory.SubFactory(PlanFactory)
    is_active = False


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    subscription = factory.SubFactory(SubscriptionFactory)
    amount = factory.Faker("random_int")
    status = Status.COMPLETED
