from django import forms
from targets.models import SavingContributions


class SavingContributionsForm(forms.ModelForm):
    class Meta:
        model = SavingContributions
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "step": "0,01",
                }
            ),
        }
