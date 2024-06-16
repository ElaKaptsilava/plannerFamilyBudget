import factory
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
    next_payment_date = factory.Faker("date")
    payment_deadline = factory.Faker("date")
    is_paid = False
