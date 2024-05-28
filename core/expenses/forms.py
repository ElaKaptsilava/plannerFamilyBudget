from django import forms

from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["category", "amount", "datetime"]
        widgets = {
            "category": forms.Select(
                attrs={"class": "form-control form-control-user text-secondary"}
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "step": "0,01",
                }
            ),
            "datetime": forms.DateInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "type": "date",
                }
            ),
        }
