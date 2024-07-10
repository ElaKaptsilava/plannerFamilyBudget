import factory
from django.utils import timezone
from incomes.models import Income


class IncomeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Income

    source = factory.Faker("company")
    category = factory.Faker("word")
    amount = factory.Faker("random_int", min=1000, max=10000)
    date = timezone.now().date()
