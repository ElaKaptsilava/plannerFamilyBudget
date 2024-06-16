import factory
from django.utils import timezone
from runningCosts.models import RunningCost, RunningCostCategory


class RunningCostCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RunningCostCategory

    name = factory.Faker("word")


class RunningCostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RunningCost

    category = factory.SubFactory(RunningCostCategoryFactory)
    name = factory.Sequence(lambda n: f"Cost {n}")
    amount = factory.Faker("random_int", min=1000, max=10000)
    period_type = RunningCost.PeriodType.MONTHS
    period = 1
    next_payment_date = timezone.now()
    payment_deadline = timezone.now() + timezone.timedelta(days=365)
    is_paid = False
