from django import forms

from .models import BudgetManager, LimitManager


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


class LimitForm(forms.ModelForm):
    class Meta:
        model = LimitManager
        fields = [
            "type",
            "category_expense",
            "category_running_cost",
            "target",
            "amount",
        ]
        widgets = {
            "type": forms.Select(
                attrs={
                    "class": "form-control form-control-user",
                    "id": "id_type",
                    "onchange": "showFields()",
                }
            ),
            "category_expense": forms.Select(
                attrs={
                    "class": "form-control form-control-user",
                    "id": "div_id_category_expense",
                }
            ),
            "category_running_cost": forms.Select(
                attrs={
                    "class": "form-control form-control-user",
                    "id": "div_id_category_running_cost",
                    "placeholder": "Select running cost category",
                }
            ),
            "target": forms.Select(
                attrs={
                    "class": "form-control form-control-user",
                    "id": "div_id_target",
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user",
                    "placeholder": "Enter amount limit",
                }
            ),
        }
