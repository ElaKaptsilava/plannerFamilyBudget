import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from multi_user.models import InvitationToken


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
