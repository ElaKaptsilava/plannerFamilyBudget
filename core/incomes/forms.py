from django import forms
from incomes.models import Income


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["source", "category", "amount", "date"]
        widgets = {
            "source": forms.TextInput(
                attrs={"class": "form-control form-control-user text-secondary"}
            ),
            "category": forms.TextInput(
                attrs={"class": "form-control form-control-user text-secondary"}
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "step": "0,01",
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "type": "date",
                }
            ),
        }
