from accounts.tests import CustomUserFactory
from budgets_manager.tests.factories import BudgetManagerFactory
from django.test import TestCase
from multi_user.tests import InvitationFactory
from subscription.tests import PlanFactory, SubscriptionFactory


class CreateInvitationViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()
        self.budget = BudgetManagerFactory.create(user=self.user)
        self.plan = PlanFactory.create(price=0)
        self.subscription = SubscriptionFactory.create(plan=self.plan, user=self.user)
        self.invitation = InvitationFactory.build()

    # @tag("test")
    # def test_create_invitation_and_send_email_success(self):
    #     self.client.force_login(self.user)
    #     invitation_data = {"email": self.invitation.email}
    #     response = self.client.post(
    #         reverse_lazy("multi_user:invitation-list-create"), data=invitation_data
    #     )
    #
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(Invitation.objects.filter(email=self.invitation.email).exists())
    #
    #     invitation = Invitation.objects.get(email=self.invitation.email)
    #     self.assertTrue(invitation.accepted)
    #     email = mail.outbox
    #     print(email)
