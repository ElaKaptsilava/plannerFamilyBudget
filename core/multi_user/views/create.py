import typing

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from multi_user.forms.family_budget import FamilyBudgetForm
from multi_user.models import FamilyBudget


class CreateFamilyBudgetView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = FamilyBudget
    form_class = FamilyBudgetForm
    template_name = "multi_user/create.html"
    success_message = "Successfully created Family Budget!"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs: dict) -> typing.Dict[str, typing.Any]:
        kwargs["form"] = self.get_form()
        return super().get_context_data(**kwargs)

    def form_valid(self, form: FamilyBudgetForm) -> FamilyBudgetForm:
        form.instance.budget_manager = self.request.user.budgetmanager
        response = super().form_valid(form)
        form.instance.members.add(self.request.user)
        return response
