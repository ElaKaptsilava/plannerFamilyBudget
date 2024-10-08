from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from incomes.models import Income


class DeleteMultipleIncomesView(LoginRequiredMixin, View):
    def post(self, request):
        selected_incomes = request.POST.getlist("selected_incomes")
        if selected_incomes:
            for income_pk in selected_incomes:
                income = Income.objects.get(pk=income_pk)
                if income.user == request.user:
                    income.delete()
                    selected_incomes.remove(income_pk)
                else:
                    messages.error(
                        request, f"You do not have permission to delete: {income!s}"
                    )
            if selected_incomes:
                messages.success(request, "Selected incomes were deleted successfully.")
        else:
            messages.error(request, "No incomes were selected.")
        return redirect(reverse_lazy("incomes:incomes-list"))
