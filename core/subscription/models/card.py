from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.db import models
from subscription.fields import CreditCardNumberField


class CreditCard(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(
        max_length=50, help_text="Enter first Name from your card."
    )
    last_name = models.CharField(
        max_length=50, help_text="Enter last Name from your card."
    )
    number = CreditCardNumberField(help_text="Enter your credit card number.")
    cvv = models.CharField(max_length=4, help_text="Enter cvv of payment.")
    valid_thru = models.DateField(help_text="Enter valid thru date.")

    def __str__(self) -> str:
        return f"{self.number[-4:]}"

    def __repr__(self) -> str:
        return f"CreditCard(owner={self.owner}, number={self.number[-4:]})"

    def clean(self):
        super().clean()
        if not self.cvv.isdigit():
            raise ValidationError("CVV must be digits.")
        if 3 > len(self.number) or len(self.number) > 4:
            raise ValidationError("Number must be 3 or 4 digits long.")
