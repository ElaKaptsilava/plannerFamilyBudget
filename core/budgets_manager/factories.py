import factory

from .models import BudgetManager
from accounts.factories import CustomUserFactory


class BudgetManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BudgetManager

    user = factory.SubFactory(CustomUserFactory)
    savings_percentage = factory.Faker("random_int", min=0, max=100)
    wants_percentage = factory.Faker("random_int", min=0, max=100)
    needs_percentage = factory.Faker("random_int", min=0, max=100)
