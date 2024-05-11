from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegistrationForm


def log_in(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("home")
        else:
            messages.error(request, "There was an error Logging In. Try again...")
    else:
        return render(request, "accounts/login.html")


class CustomLoginView(LoginView):
    # authentication_form = CustomUserLoginForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("home")
    redirect_authenticated_user = True
    redirect_field_name = reverse_lazy("home")


class RegisterView(CreateView):
    template_name = "accounts/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("home")
