from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from .forms import (
    AccountAuthenticationForm,
    CustomUserUpdateForm,
    ProfileForm,
    RegistrationForm,
)
from .models import CustomUser


class CustomLoginView(View):
    template_name: str = "registration/login.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        context: dict = {}
        user: CustomUser = request.user
        if user.is_authenticated:
            return redirect(reverse_lazy("home", kwargs={"user_id": user.pk}))
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
                return redirect(reverse_lazy("home", kwargs={"user_id": user.id}))
        context["login_form"] = form
        return render(request, template_name=self.template_name, context=context)


class CustomRegisterView(View):
    template_name: str = "registration/register.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        user: CustomUser = request.user
        if user.is_authenticated:
            return redirect("accounts:login")
        return render(
            request,
            template_name=self.template_name,
            context={"registration_form": RegistrationForm()},
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
                    reverse_lazy("home", kwargs={"user_id": user_authenticate.id})
                )
        return render(
            request,
            template_name=self.template_name,
            context={"registration_form": form},
        )


class CustomResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name: str = "registration/reset_password.html"
    email_template_name: str = "registration/password_reset_email.html"
    subject_template_name: str = "registration/password_reset_subject.txt"
    success_message: str = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )

    def form_valid(self, form) -> HttpResponse:
        """
        If the form is valid, send a password reset email to the user.
        """
        form.save(
            subject_template_name=self.subject_template_name,
            email_template_name=self.email_template_name,
            html_email_template_name=self.html_email_template_name,
            request=self.request,
            token_generator=self.token_generator,
            from_email=self.from_email,
        )
        messages.success(self.request, self.success_message)
        return self.render_to_response(self.get_context_data(form=form))


class ProfileView(LoginRequiredMixin, View):
    template_name: str = "accounts/profile.html"
    login_url: reverse_lazy = reverse_lazy("accounts:login")

    def get(self, request, user_id: int) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(
            request,
            template_name=self.template_name,
            context={"user_form": user_form, "profile_form": profile_form},
        )

    def post(self, request, user_id: int) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, "Your profile has been updated successfully")
            return redirect(
                reverse_lazy("accounts:profile", kwargs={"user_id": request.user.id})
            )

        messages.error(request, "Error updating you profile")

        return render(
            request,
            template_name=self.template_name,
            context={"user_form": user_form, "profile_form": profile_form},
        )


class HomeView(LoginRequiredMixin, View):
    template_name: str = "accounts/dashboard.html"
    login_url: reverse_lazy = reverse_lazy("accounts:login")
    http_method_names: list = ["get"]

    def get(self, request, user_id: int) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        return render(request, self.template_name, {"user_id": user_id})
