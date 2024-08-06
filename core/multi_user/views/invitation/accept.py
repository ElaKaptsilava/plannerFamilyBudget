from django.shortcuts import get_object_or_404, redirect
from django.views import View
from multi_user.models import Invitation


class AcceptInvitationView(View):
    def get(self, request, token, *args, **kwargs):
        invitation = get_object_or_404(Invitation, token=token, accepted=True)
        print(invitation)
        print(token)
        return redirect("register_with_invite") + f"?token={token}"
