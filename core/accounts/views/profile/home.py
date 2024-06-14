from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class HomeView(LoginRequiredMixin, View):
    template_name: str = "accounts/dashboard.html"
    http_method_names: list = ["get"]

    def get(self, request, user_id: int) -> HttpResponse:
        return render(request, self.template_name, {"user_id": user_id})
