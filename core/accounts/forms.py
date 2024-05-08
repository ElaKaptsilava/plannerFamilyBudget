from django import forms
from django.contrib.auth.forms import AuthenticationForm

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

    class Meta:
        model = CustomUser
        fields = ["username", "password"]


class CustomUserRegisterForm(AuthenticationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "exampleFirstName",
                "placeholder": "First name",
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "exampleLastName",
                "placeholder": "Last name",
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "exampleInputEmail",
                "placeholder": "Email Address",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "exampleInputPassword",
                "placeholder": "Password",
            }
        )
    )
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "exampleRepeatPassword",
                "placeholder": "Repeat password",
            }
        )
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
