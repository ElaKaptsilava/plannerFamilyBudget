from accounts.forms import AccountAuthenticationForm
from budgets_manager.utils import check_is_user_has_budget
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import RedirectURLMixin
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy
from django.views.generic import FormView
from subscription.utils import check_is_user_has_subscription


class CustomLoginView(RedirectURLMixin, FormView):
    form_class = AccountAuthenticationForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("home")

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(email=email, password=password)

        if user is not None:
            login(self.request, user)
            if budget_create_url := check_is_user_has_budget(request=self.request):
                return redirect(budget_create_url)
            if subscription_url := check_is_user_has_subscription(request=self.request):
                return redirect(subscription_url)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid email or password.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, form.errors.get(None, "Invalid email or password.")
        )
        return response
