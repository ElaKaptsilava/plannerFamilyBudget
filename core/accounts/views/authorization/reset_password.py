from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse


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
