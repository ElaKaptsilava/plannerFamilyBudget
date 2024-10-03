import factory
from accounts.tests import CustomUserFactory
from budgets_manager.constants import TODAY
from expenses.models import Expense, ExpenseCategory
from expenses.types import Type


class ExpenseCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExpenseCategory

    user = factory.SubFactory(CustomUserFactory)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    type = Type.NEEDS


class ExpenseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Expense

    user = factory.SubFactory(CustomUserFactory)
    category = factory.SubFactory(ExpenseCategoryFactory)
    amount = factory.Faker("random_int", min=1000, max=10000)
    datetime = TODAY
