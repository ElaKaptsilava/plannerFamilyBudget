from accounts.forms import AccountAuthenticationForm
from accounts.models import CustomUser
from budgets_manager.utils import check_is_user_has_budget
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from subscription.utils import check_is_user_has_subscription


class CustomLoginView(View):
    template_name: str = "registration/login.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        context: dict = {}
        user: CustomUser = request.user
        if not user.is_authenticated:
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
            if authenticate_user := authenticate(email=email, password=password):
                login(request, authenticate_user)
                budget_create_url = check_is_user_has_budget(request=request)
                if budget_create_url:
                    return redirect(budget_create_url)
                if subscription_url := check_is_user_has_subscription(request=request):
                    return redirect(subscription_url)
                messages.success(request, f"Welcome back, {authenticate_user.email}!")
                return redirect(reverse_lazy("home"))
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(
                request, "Invalid form submission. Please check the entered data."
            )
        context["login_form"] = form
        return render(request, template_name=self.template_name, context=context)
