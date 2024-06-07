import factory
from accounts.factories import CustomUserFactory

from .models import Target, TargetContribution


class TargetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Target

    user = factory.SubFactory(CustomUserFactory)
    target = factory.Faker("word")
    amount = factory.Faker("random_int", min=1000, max=10000)
    description = factory.Faker("text")
    deadline = factory.Faker("date")


class TargetContributionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TargetContribution

    user = factory.SubFactory(CustomUserFactory)
    target = factory.SubFactory(TargetFactory)
    amount = factory.Faker("random_int", min=1000, max=10000)
