from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from incomes.forms import IncomeForm
from incomes.models import Income


class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    form_class = IncomeForm
    model = Income
    success_url = reverse_lazy("incomes:incomes-list")
    context_object_name = "incomes"
    template_name: str = "incomes/incomes.html"

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to update the income. Please check the form."
        )
        return HttpResponseRedirect(self.success_url)

    def form_valid(self, form) -> HttpResponseRedirect:
        """If the form is valid, save the associated model."""
        self.object = form.save()
        response = super().form_valid(form)
        messages.success(self.request, "The income updated successfully!")
        return response
