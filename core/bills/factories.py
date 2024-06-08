import factory
from bills.models import Bill


class BillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bill

    creditor = factory.Faker("last_name")
    amount = factory.Faker("pyfloat", min_value=1000, max_value=100000)
    deadline = factory.Faker("date")
