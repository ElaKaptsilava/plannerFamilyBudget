from django import forms

from .models import BudgetManager


class BudgetForm(forms.ModelForm):
    class Meta:
        model = BudgetManager
        fields = ["savings_percentage", "needs_percentage", "wants_percentage"]

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop("user")
    #     super().__init__(*args, **kwargs)
    #     self.fields["category_expense"].queryset = RunningCostCategory.objects.filter(
    #         user=user
    #     )
    #     self.fields["category_running_cost"].queryset = ExpenseCategory.objects.filter(
    #         user=user
    #     )
