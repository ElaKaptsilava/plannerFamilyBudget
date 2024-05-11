from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import AccountAuthenticationForm, RegistrationForm


def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    destination = get_redirect_if_exists(request)

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context["login_form"] = form

    return render(request, "accounts/login.html", context)


def get_redirect_if_exists(request):
    redirect_ = None
    if request.GET:
        if request.GET.get("next"):
            redirect_ = str(request.GET.get("next"))
    return redirect_


class RegisterView(CreateView, SuccessMessageMixin):
    template_name = "accounts/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("accounts:login")
    success_message = "You have successfully registered."
