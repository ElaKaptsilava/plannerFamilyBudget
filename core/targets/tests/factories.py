import factory
from accounts.tests import CustomUserFactory
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from targets.models import Target, TargetContribution


class TargetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Target

    user = factory.SubFactory(CustomUserFactory)
    target = factory.Faker("word")
    amount = factory.Faker("random_int", min=1000, max=10000)
    description = factory.Faker("text")
    deadline = timezone.now().date() + relativedelta(years=1)


class TargetContributionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TargetContribution

    user = factory.SubFactory(CustomUserFactory)
    target = factory.SubFactory(TargetFactory)
    amount = factory.Faker("random_int", min=1000, max=10000)
