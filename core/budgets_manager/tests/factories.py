import factory
from accounts.tests import CustomUserFactory
from budgets_manager.models import BudgetManager, LimitManager


class BudgetManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BudgetManager

    user = factory.SubFactory(CustomUserFactory)
    savings_percentage = 20
    wants_percentage = 40
    needs_percentage = 40


class LimitManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LimitManager

    amount = factory.Faker("pyint")
