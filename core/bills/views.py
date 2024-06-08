from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import BillForm
from .models import Bill


class BillFormView(LoginRequiredMixin, FormView):
    model = Bill
    form_class = BillForm
    template_name = "bills/bills.html"
    success_url = reverse_lazy("bills:bills-list")
    context_object_name = "bills"

    def form_valid(self, form):
        bill = form.save(commit=False)
        bill.user = self.request.user
        bill.save()
        messages.success(self.request, "The bill added successfully!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form) -> HttpResponseRedirect:
        messages.error(self.request, "TFailed to add bills. Please check the form.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["object_list"] = self.model.objects.filter(user=self.request.user)
        return context
