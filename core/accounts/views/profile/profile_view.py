from accounts.forms import CustomUserUpdateForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View


class ProfileView(LoginRequiredMixin, View):
    template_name: str = "accounts/profile.html"
    login_url: reverse_lazy = reverse_lazy("accounts:login")

    def get(self, request, user_id: int) -> HttpResponse:
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(
            request,
            template_name=self.template_name,
            context={"user_form": user_form, "profile_form": profile_form},
        )

    def post(self, request, user_id: int) -> HttpResponse:
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
