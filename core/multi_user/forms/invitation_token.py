from django import forms
from multi_user.models import InvitationToken


class InvitationTokenForm(forms.ModelForm):
    class Meta:
        model = InvitationToken
        fields = ["email"]
