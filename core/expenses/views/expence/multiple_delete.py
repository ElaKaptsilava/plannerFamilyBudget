from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from expenses.models import Expense


class DeleteMultipleExpenseView(LoginRequiredMixin, View):
    def post(self, request):
        selected_expenses = request.POST.getlist("selected_expenses")
        if selected_expenses:
            Expense.objects.filter(id__in=selected_expenses).delete()
            messages.success(request, "Selected expenses were deleted successfully.")
        else:
            messages.info(request, "No expenses were selected.")
        return HttpResponseRedirect(reverse_lazy("expenses:expenses-list"))
