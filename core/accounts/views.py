from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .forms import AccountAuthenticationForm, RegistrationForm


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("accounts:login")

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email").lower()
            raw_password = form.cleaned_data.get("password1")
            user_authenticate = authenticate(email=email, password=raw_password)
            login(request, user_authenticate)
            return redirect("home")
        else:
            context["registration_form"] = form

    else:
        form = RegistrationForm()
        context["registration_form"] = form
    return render(request, "accounts/register.html", context)


def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context["login_form"] = form

    return render(request, "accounts/login.html", context)
