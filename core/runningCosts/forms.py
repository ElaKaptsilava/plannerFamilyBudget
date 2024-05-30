from django import forms

from .models import RunningCost, RunningCostCategory


class RunningCostForm(forms.ModelForm):
    class Meta:
        model = RunningCost
        fields = [
            "name",
            "category",
            "amount",
            "period_type",
            "period",
            "next_payment_date",
            "payment_deadline",
            "is_paid",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control form-control-user text-secondary"}
            ),
            "category": forms.Select(
                attrs={"class": "form-control form-control-user text-secondary"}
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "step": "0,01",
                }
            ),
            "period_type": forms.Select(
                attrs={"class": "form-control form-control-user text-secondary"}
            ),
            "period": forms.NumberInput(
                attrs={"class": "form-control form-control-user text-secondary"}
            ),
            "next_payment_date": forms.DateInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "type": "date",
                }
            ),
            "payment_deadline": forms.DateInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "type": "date",
                }
            ),
            "is_paid": forms.CheckboxInput(
                attrs={"class": "form-control form-control-user text-secondary"}
            ),
            "is_overdue": forms.CheckboxInput(
                attrs={"class": "form-control form-control-user text-secondary"}
            ),
        }


class RunningCostCategoryForm(forms.ModelForm):
    class Meta:
        model = RunningCostCategory
        fields = ["name", "description"]
