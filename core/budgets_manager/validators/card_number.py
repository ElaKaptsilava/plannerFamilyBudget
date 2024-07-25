from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from subscription.algorithms import LuhnAlgorithm


class CreditCardField(forms.CharField):
    default_error_messages = {
        "invalid": "Enter a valid credit card number.",
    }

    def clean(self, value):
        value = super().clean(value)
        luhn = LuhnAlgorithm(value)
        if not luhn.verify():
            raise ValidationError(self.error_messages["invalid"], code="invalid")
        return value


class CreditCardNumberField(models.CharField):
    description = "Credit Card Number"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 19
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.update({"form_class": CreditCardField})
        return super().formfield(**kwargs)
