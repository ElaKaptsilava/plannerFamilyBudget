from django import forms
from incomes.models import Income


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["source", "category", "amount", "date"]
        widgets = {
            "source": forms.TextInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "placeholder": "Enter source",
                }
            ),
            "category": forms.TextInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "placeholder": "Enter category",
                }
            ),
            "amount": forms.TextInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "placeholder": "Enter amount",
                }
            ),
            "date": forms.DateTimeInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "id": "datetime",
                    "placeholder": "Enter date",
                }
            ),
        }
