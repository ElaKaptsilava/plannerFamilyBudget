import factory


class BillFactory(factory.django.DjangoModelFactory):
    creditor = factory.Faker("first_name")
    amount = factory.Faker("random_int", min_value=1000, max_value=1000000)
    deadline = factory.Faker("date")
