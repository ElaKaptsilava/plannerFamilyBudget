from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .forms import CustomUserLoginForm, CustomUserRegisterForm


def login_view(request):
    if request.method == "POST":
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form, "error": "Invalid login credentials."},
                )
    else:
        form = CustomUserLoginForm()
    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})
