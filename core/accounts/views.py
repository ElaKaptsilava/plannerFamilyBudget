from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegistrationForm


class CustomLoginView(LoginView, SuccessMessageMixin):
    template_name = "accounts/login.html"
    success_url = reverse_lazy("home")
    redirect_authenticated_user = True
    success_message = "You have successfully logged in."

    def get_redirect_url(self):
        return reverse_lazy("home")

    def form_invalid(self, form):
        messages.error(self.request, "Please try again.")
        return redirect("accounts:login")


class RegisterView(CreateView, SuccessMessageMixin):
    template_name = "accounts/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("accounts:login")
    success_message = "You have successfully registered."
