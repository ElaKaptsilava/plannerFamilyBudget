import factory
from accounts.tests import CustomUserFactory
from budgets_manager.tests.factories.budget_manager_factory import BudgetManagerFactory
from django.utils import timezone
from incomes.models import Income


class IncomeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Income

    user = factory.SubFactory(CustomUserFactory)
    budget = factory.SubFactory(BudgetManagerFactory)
    source = factory.Faker("company")
    category = factory.Faker("word")
    amount = factory.Faker("random_int", min=1000, max=10000)
    date = timezone.now().date()
