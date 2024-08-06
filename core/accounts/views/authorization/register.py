from accounts.forms import RegistrationForm
from accounts.models import CustomUser
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View


class CustomRegisterView(View):
    template_name: str = "registration/register.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        user: CustomUser = request.user
        if user.is_authenticated:
            return redirect("accounts:login")
        context = {"registration_form": RegistrationForm()}
        return render(
            request,
            template_name=self.template_name,
            context=context,
        )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        user: CustomUser = request.user
        if user.is_authenticated:
            return redirect("accounts:login")

        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email: str = form.cleaned_data.get("email").lower()
            raw_password: str = form.cleaned_data.get("password1")
            user_authenticate: authenticate = authenticate(
                email=email, password=raw_password
            )
            if user_authenticate:
                login(request, user_authenticate)
                return redirect(
                    reverse_lazy(
                        "manager:budget-list-create",
                    )
                )
        return render(
            request,
            template_name=self.template_name,
            context={"registration_form": form},
        )
