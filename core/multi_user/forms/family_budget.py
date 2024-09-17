from colorfield.widgets import ColorWidget
from django import forms
from multi_user.models import FamilyBudget


class FamilyBudgetForm(forms.ModelForm):
    class Meta:
        model = FamilyBudget
        fields = ["title", "color"]
        widgets = {
            "color": ColorWidget(),
        }
