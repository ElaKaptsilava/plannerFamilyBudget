import factory
from accounts.factories import CustomUserFactory
from budgets_manager.models import BudgetManager


class BudgetManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BudgetManager

    user = factory.SubFactory(CustomUserFactory)
    savings_percentage = 20
    wants_percentage = 40
    needs_percentage = 40
