import factory
from budgets_manager.constants import TODAY
from expenses.models import Expense, ExpenseCategory
from expenses.types import Type


class ExpenseCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExpenseCategory

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    type = Type.NEEDS


class ExpenseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Expense

    category = factory.SubFactory(ExpenseCategoryFactory)
    amount = factory.Faker("random_int", min=1000, max=10000)
    datetime = TODAY
