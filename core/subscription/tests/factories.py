import factory
from accounts.tests import CustomUserFactory
from budgets_manager.constants import TODAY
from dateutil.relativedelta import relativedelta

from ..models import CreditCard, Payment, Plan, Subscription


class PlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plan

    name = factory.Sequence(lambda n: f"plan {n}")
    price = factory.Faker("random_int")
    description = factory.Faker("text")


class CreditCardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CreditCard

    owner = factory.SubFactory(CustomUserFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    number = "4111 1111 1111 1111"
    cvv = "1111"
    valid_thru = TODAY.date() + relativedelta(months=3)


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    user = factory.SubFactory(CustomUserFactory)
    plan = factory.SubFactory(PlanFactory)


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    subscription = factory.SubFactory(SubscriptionFactory)
