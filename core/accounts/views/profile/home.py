from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class HomeView(LoginRequiredMixin, View):  # TemplateView
    template_name: str = "accounts/dashboard.html"
    http_method_names: list = ["get"]

    def get(self, request) -> HttpResponse:
        return render(request, self.template_name)
