from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class CustomUserLoginForm(AuthenticationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "exampleInputEmail",
                "aria-describedby": "emailHelp",
                "placeholder": "Enter Email Address...",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "exampleInputPassword",
                "aria-describedby": "passwordHelp",
                "placeholder": "Password",
            }
        )
    )

    def clean(self):
        super().clean()
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        self.user_cache = authenticate(self.request, email=email, password=password)
        if not self.user_cache:
            raise forms.ValidationError("Invalid email or password")
        return self.cleaned_data


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "username"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
