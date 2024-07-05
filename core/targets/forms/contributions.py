from django import forms
from targets.models import TargetContribution


class TargetContributionForm(forms.ModelForm):
    class Meta:
        model = TargetContribution
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "step": "0,01",
                }
            ),
        }
