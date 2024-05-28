import factory

from .models import RunningCost, RunningCostCategory


class RunningCostCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RunningCostCategory

    name = factory.Sequence(lambda n: f"Category {n}")


class RunningCostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RunningCost

    category = factory.SubFactory(RunningCostCategoryFactory)
    name = factory.Sequence(lambda n: f"Cost {n}")
    amount = factory.Faker("random_int", min=1000, max=10000)
    period_type = RunningCost.PeriodType.MONTHS
    period = 1
    due_date = factory.Faker("date")
    payment_deadline = factory.Faker("date")
    is_paid = False
