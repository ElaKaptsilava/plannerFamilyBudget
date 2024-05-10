from django import forms
from django.contrib.auth import authenticate
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

    def clean(self):
        super().clean()
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        self.user_cache = authenticate(self.request, email=email, password=password)
        if not self.user_cache:
            raise forms.ValidationError("Invalid email or password")
        print(self.cleaned_data)
        return self.cleaned_data


# class CustomUserLoginForm(forms.ModelForm):
#     email = forms.EmailField(
#         widget=forms.EmailInput(
#             attrs={
#                 "class": "form-control form-control-user",
#                 "id": "exampleInputEmail",
#                 "aria-describedby": "emailHelp",
#                 "placeholder": "Enter Email Address...",
#             }
#         )
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 "class": "form-control form-control-user",
#                 "id": "exampleInputPassword",
#                 "aria-describedby": "passwordHelp",
#                 "placeholder": "Password",
#             }
#         )
#     )
#
#     class Meta:
#         model = CustomUser
#         fields = ["email", "password"]
#
#     def clean_email(self):
#         print(self.cleaned_data)
#         email = self.cleaned_data.get('email')
#         if not CustomUser.objects.filter(email=email).exists():
#             raise forms.ValidationError('This email address is not associated with an account.')
#         return email


class CustomUserRegisterForm(forms.Form):
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
