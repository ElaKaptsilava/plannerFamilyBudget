import typing
import uuid

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from ...forms.invitation import InvitationForm
from ...models import Invitation
from ...tasks import sending_email


class CreateInvitationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Invitation
    form_class = InvitationForm
    template_name = "multi_user/invitation/create.html"
    success_url = reverse_lazy("home")
    success_message = "Invitation created successfully."
    error_message = "Invitation creation failed."

    def generate_token(self) -> str:
        token = str(uuid.uuid4())
        while self.get_queryset().filter(token=token).exists():
            token = str(uuid.uuid4())
        return token

    def get_queryset(self) -> QuerySet[Invitation]:
        return super().get_queryset().filter(budget=self.request.user.budgetmanager)

    def get_context_data(
        self, **kwargs: dict[str, typing.Any]
    ) -> dict[str, typing.Any]:
        context = super().get_context_data(**kwargs)
        context["invitation_form"] = InvitationForm()
        print(context)
        return context

    def form_valid(self, form: InvitationForm) -> HttpResponse:
        self.object = form.save(commit=False)
        token = self.generate_token()

        self.object.budget = self.request.user.budgetmanager
        self.object.token = token
        self.object.save()

        invitation_link = self.request.build_absolute_uri(
            f"multiuser/accept_invite/{token}"
        )
        params = {"invitation_link": invitation_link, "invitation_id": self.object.pk}

        if not form.instance.accepted:
            transaction.on_commit(lambda: sending_email.delay(params))
            self.object.accepted = True
        return super().form_valid(form)

    def form_invalid(self, form: InvitationForm) -> HttpResponse:
        messages.error(self.request, self.error_message)
        print("form invalid")
        return super().form_valid(form)
