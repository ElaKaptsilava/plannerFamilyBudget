from django import forms

from .models import BudgetManager


class BudgetManagerForm(forms.ModelForm):
    class Meta:
        model = BudgetManager
        fields = ["savings_percentage", "needs_percentage", "wants_percentage"]
        widgets = {
            "savings_percentage": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user",
                    "value": 20.0,
                    "step": 1.0,
                }
            ),
            "needs_percentage": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user",
                    "value": 40.0,
                    "step": 1.0,
                }
            ),
            "wants_percentage": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user",
                    "value": 40.0,
                    "step": 1.0,
                }
            ),
        }
