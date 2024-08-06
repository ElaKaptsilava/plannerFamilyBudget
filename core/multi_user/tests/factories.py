import factory
from multi_user.models import Invitation


class InvitationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invitation

    email = factory.Sequence(lambda n: f"email{n}@gmail.com")
