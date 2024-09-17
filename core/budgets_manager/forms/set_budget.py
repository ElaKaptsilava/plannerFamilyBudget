from budgets_manager.models import SetBudget
from django import forms


class SetBudgetForm(forms.ModelForm):
    class Meta:
        model = SetBudget
        fields = ["budget"]
