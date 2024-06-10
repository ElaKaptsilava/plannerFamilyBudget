from budgets_manager.forms import BudgetManagerForm
from budgets_manager.models import BudgetManager
from django.views.generic import CreateView


class BudgetManagerFormViewSet(CreateView):
    form_class = BudgetManagerForm
    template_name = "budgets_manager/budgets_manager.html"
    context_object_name = "budget"
    model = BudgetManager

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["object_list"] = self.model.objects.filter(user=self.request.user)
        return context
