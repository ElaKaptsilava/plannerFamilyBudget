from django import forms
from incomes.models import Income


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["source", "category", "amount", "date"]


class IncomesFilterForm(forms.Form):
    min_amount = forms.DecimalField(required=False, min_value=0, label="Min Amount")
    max_amount = forms.DecimalField(required=False, min_value=0, label="Max Amount")
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Start Date",
    )
    end_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"}), label="End Date"
    )
