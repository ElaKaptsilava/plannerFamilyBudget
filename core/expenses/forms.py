from django import forms

from .models import Expense, ExpenseCategory


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["category", "amount", "datetime"]


class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ["name"]


class ExpenseFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=ExpenseCategory.objects.all(), required=False, label="Category"
    )
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
