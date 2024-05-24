from django import forms

from .models import RunningCost, RunningCostCategory


class RunningCostForm(forms.ModelForm):
    class Meta:
        model = RunningCost
        fields = ["name", "category", "amount", "period_type", "period", "due_date"]


class RunningCostCategoryForm(forms.ModelForm):
    class Meta:
        model = RunningCostCategory
        fields = ["name", "description"]
