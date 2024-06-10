from django import forms

from .models import BudgetManager


class BudgetManagerForm(forms.ModelForm):
    class Meta:
        model = BudgetManager
        fields = ["savings_percentage", "needs_percentage", "wants_percentage"]
