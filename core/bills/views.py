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

    def form_invalid(self, form):
        messages.success(self.request, "TFailed to add bills. Please check the form.")
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
            kwargs["object_list"] = self.model.objects.filter(user=self.request.user)
        return super().get_context_data(**kwargs)
