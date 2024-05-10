from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import CustomUserLoginForm, CustomUserRegisterForm


def index(request):
    return render(request, "accounts/index.html")


class CustomLoginView(LoginView):
    authentication_form = CustomUserLoginForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("home")

    # def get_form_kwargs(self):
    #     """
    #     Returns the keyword arguments for instantiating the form.
    #     """
    #     kwargs = super().get_form_kwargs()
    #     kwargs.pop('request', None)
    #     return kwargs
    #
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     print(form.errors)
    #     if form.is_valid():
    #         try:
    #             email = form.cleaned_data.get('email')
    #             password = form.cleaned_data.get('password')
    #             if email and password:
    #                 user = CustomUser.objects.get(email=email)
    #                 if user.check_password(password):
    #                     user.is_active = True
    #                     user.save()
    #                     login(request, user)
    #                     return redirect(self.success_url)
    #         except CustomUser.DoesNotExist:
    #             return self.form_invalid(form)
    #     return render(request, self.template_name, context={'form': self.form_class})


def register_view(request):
    if request.method == "POST":
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})
