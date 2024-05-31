from django import forms

from .models import Target, TargetContribution


class TargetForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = ["target", "amount", "deadline"]
        widgets = {
            "target": forms.TextInput(
                attrs={"class": "form-control form-control-user text-secondary"}
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "step": 0.01,
                }
            ),
            "deadline": forms.DateInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "type": "date",
                }
            ),
        }


class TargetContributionForm(forms.ModelForm):
    class Meta:
        model = TargetContribution
        fields = ["target", "amount"]
        widgets = {
            "target": forms.Select(
                attrs={"class": "form-control form-control-user text-secondary"}
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "step": "0,01",
                }
            ),
        }
