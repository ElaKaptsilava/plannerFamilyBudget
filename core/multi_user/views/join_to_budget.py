import uuid

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from multi_user.models import FamilyBudget, InvitationToken


@login_required
def invite_family_member(request, family_budget_id):
    family_budget = get_object_or_404(
        FamilyBudget, id=family_budget_id, owner=request.user
    )

    if request.method == "POST":
        email: str = request.POST.get("email")
        if InvitationToken.objects.filter(
            family_budget=family_budget, email=email, is_used=False
        ).exists():
            return HttpResponse(
                f"An invitation has already been sent to {email}.", status=400
            )

        invitation = InvitationToken.objects.create(
            token=uuid.uuid4(), family_budget=family_budget, email=email
        )

        invitation_link = request.build_absolute_uri(  # noqa:F841
            reverse("multiuser:invite-list-accept", args=[invitation.token])
        )

        subject = _("You've been invited to join a family budget")
        body = _("Click the link to join the family budget: {invitation_link}")
        send_mail(
            subject=subject,
            message=body,
            from_email="no-reply@familybudget.com",
            recipient_list=[email],
        )

        return HttpResponse(f"Invitation sent to {email}.")

    return render(request, "multi_user/send.html", {"family_budget": family_budget})


@login_required
def join_family_budget(request, token):
    try:
        token_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse("Invalid invitation token", status=400)

    invitation = get_object_or_404(InvitationToken, token=token_uuid, is_used=False)

    if request.method == "POST":
        if request.user.is_authenticated:
            family_budget = invitation.family_budget
            family_budget.members.add(request.user)

            invitation.is_used = True
            invitation.save()

            return redirect(reverse_lazy("home"))
        else:
            return redirect(
                f"{reverse_lazy('accounts:login')}?next=/accept_invite/{token}/"
            )

    return render(request, "multi_user/accept.html", {"invitation": invitation})
