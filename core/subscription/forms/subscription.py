from django import forms
from subscription.models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["plan"]
        widgets = {
            "plan": forms.RadioSelect,
        }
