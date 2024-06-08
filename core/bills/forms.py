from bills.models import Bill
from django import forms


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ["creditor", "amount", "deadline"]
        widgets = {
            "creditor": forms.TextInput(
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
