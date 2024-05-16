from django import forms
from incomes.models import Income


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["source", "category", "amount", "date"]
