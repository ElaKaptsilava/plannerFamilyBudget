from django import forms
from targets.models import SavingContributions


class SavingPositiveContributionsForm(forms.ModelForm):
    class Meta:
        model = SavingContributions
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "step": "0,1",
                    "min": "0",
                }
            ),
        }


class SavingNegativeContributionsForm(forms.ModelForm):
    class Meta:
        model = SavingContributions
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "step": "0.1",
                    "max": "-1",
                }
            ),
        }
