import factory

from .models import Expense, ExpenseCategory


class ExpenseCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExpenseCategory

    name = factory.Faker("word")
    description = factory.Faker("sentence")


class IncomeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Expense

    category = factory.SubFactory(ExpenseCategoryFactory)
    amount = factory.Faker("random_int", min=1000, max=10000)
    datetime = factory.Faker("date_time_between", start_date="-1y", end_date="now")
