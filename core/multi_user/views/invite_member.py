import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView
from multi_user.forms.invitation_token import InvitationTokenForm
from multi_user.models import FamilyBudget, InvitationToken


class InviteMemberView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = InvitationToken
    success_url = reverse_lazy("home")
    template_name = "multi_user/send.html"
    form_class = InvitationTokenForm

    def get_success_message(self, cleaned_data):
        return _(
            f'Invitation token has been successfully send to {cleaned_data["email"]}.'
        )

    def form_valid(self, form):
        family_budget = FamilyBudget.objects.get(pk=self.kwargs["family_budget_id"])
        form.instance.family_budget = family_budget
        form.instance.token = uuid.uuid4()
        response = super().form_valid(form)

        invitation_link = self.request.build_absolute_uri(
            reverse("multiuser:invite-list-accept", args=[self.object.token])
        )

        subject = _("You've been invited to join a family budget")
        body = _(f"Click the link to join the family budget: {invitation_link}")

        send_mail(
            subject=subject,
            message=body,
            from_email="no-reply@familybudget.com",
            recipient_list=[self.object.email],
        )

        return response
