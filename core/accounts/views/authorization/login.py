from accounts.forms import AccountAuthenticationForm
from accounts.models import CustomUser
from budgets_manager.utils import check_and_redirect_to_budget_create
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View


class CustomLoginView(View):
    template_name: str = "registration/login.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        context: dict = {}
        user: CustomUser = request.user
        if user.is_authenticated:
            messages.info(request, f"You are already logged in as {user.email}.")
            check_and_redirect_to_budget_create(request)
            return redirect(reverse_lazy("home"))
        else:
            messages.info(request, "Please log in to continue.")
        form = AccountAuthenticationForm()
        context["login_form"] = form
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        context: dict = {}
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email: str = form.cleaned_data["email"]
            password: str = form.cleaned_data["password"]
            user: authenticate = authenticate(email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.email}!")
                check_and_redirect_to_budget_create(request)
                return redirect(reverse_lazy("home"))
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(
                request, "Invalid form submission. Please check the entered data."
            )
        context["login_form"] = form
        return render(request, template_name=self.template_name, context=context)
