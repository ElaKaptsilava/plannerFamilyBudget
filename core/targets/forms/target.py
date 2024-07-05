from django import forms
from targets.models import Target


class TargetForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = ["target", "amount", "deadline", "image", "description"]
        widgets = {
            "target": forms.TextInput(
                attrs={"class": "form-control form-control-user text-secondary"}
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "step": 0.01,
                }
            ),
            "deadline": forms.DateInput(
                attrs={
                    "class": "form-control form-control-user text-secondary",
                    "type": "date",
                }
            ),
            "image": forms.FileInput(
                attrs={"class": "form-control-user text-secondary"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control form-control-user text-secondary"}
            ),
        }
