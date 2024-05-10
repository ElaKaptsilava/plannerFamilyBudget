from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import CustomUserLoginForm, CustomUserRegisterForm


def index(request):
    return render(request, "accounts/index.html")


class CustomLoginView(LoginView):
    authentication_form = CustomUserLoginForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("accounts:home")


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
