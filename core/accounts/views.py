from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from .forms import (
    AccountAuthenticationForm,
    CustomUserUpdateForm,
    ProfileForm,
    RegistrationForm,
)


class CustomLoginView(View):
    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        context = {}
        user = request.user
        if user.is_authenticated:
            return redirect(reverse_lazy("home", kwargs={"user_id": user.id}))
        form = AccountAuthenticationForm()
        context["login_form"] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect(reverse_lazy("home", kwargs={"user_id": user.id}))
        context["login_form"] = form
        return render(request, self.template_name, context)


class CustomRegisterView(View):
    template_name = "registration/register.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return redirect("accounts:login")
        context = {"registration_form": RegistrationForm()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return redirect("accounts:login")

        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email").lower()
            raw_password = form.cleaned_data.get("password1")
            user_authenticate = authenticate(email=email, password=raw_password)
            login(request, user_authenticate)
            return redirect(
                reverse_lazy("home", kwargs={"user_id": user_authenticate.id})
            )
        else:
            context = {"registration_form": form}
            return render(request, self.template_name, context)


class CustomResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "registration/reset_password.html"
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject.txt"
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )

    def form_valid(self, form):
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


class CustomResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = ("registration/reset_password_confirm.html",)
    success_url = reverse_lazy("accounts:password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"


class ProfileView(LoginRequiredMixin, View):
    template_name: str = "accounts/profile.html"

    def get(self, request, user_id):
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

        context = {"user_form": user_form, "profile_form": profile_form}

        return render(request, self.template_name, context)

    def post(self, request, user_id):
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
        else:
            context = {"user_form": user_form, "profile_form": profile_form}
            messages.error(request, "Error updating you profile")

            return render(request, self.template_name, context)
