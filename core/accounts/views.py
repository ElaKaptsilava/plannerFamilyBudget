from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render

from .forms import AccountAuthenticationForm, RegistrationForm


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("accounts:login")

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email").lower()
            raw_password = form.cleaned_data.get("password1")
            user_authenticate = authenticate(email=email, password=raw_password)
            login(request, user_authenticate)
            return redirect("home")
        else:
            print(form.errors)
            context["registration_form"] = form

    else:
        form = RegistrationForm()
        context["registration_form"] = form
    return render(request, "accounts/register.html", context)


def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

        context["login_form"] = form

    return render(request, "accounts/login.html", context)


class CustomResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "accounts/forgot-password.html"
    email_template_name = "accounts/password-reset-email.html"
    subject_template_name = "accounts/password-reset-subject.txt"
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
