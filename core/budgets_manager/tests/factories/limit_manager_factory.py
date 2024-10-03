import factory
from budgets_manager.models import LimitManager
from budgets_manager.tests.factories.budget_manager_factory import BudgetManagerFactory


class LimitManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LimitManager

    budget_manager = factory.SubFactory(BudgetManagerFactory)
    amount = factory.Faker("pyint")
