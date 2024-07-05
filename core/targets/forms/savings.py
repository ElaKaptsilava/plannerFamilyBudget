from django import forms
from targets.models import SavingContributions


class SavingPositiveContributionsForm(forms.ModelForm):
    class Meta:
        model = SavingContributions
        fields = ["positive_amount"]
        widgets = {
            "positive_amount": forms.NumberInput(
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
        fields = ["negative_amount"]
        widgets = {
            "negative_amount": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "step": "0.1",
                    "max": "-1",
                }
            ),
        }
