from budgets_manager.forms import LimitForm
from budgets_manager.models import LimitManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView


class LimitListView(LoginRequiredMixin, ListView):
    model = LimitManager
    template_name = "budgets_manager/limits/list.html"
    context_object_name = "limit"

    def get_queryset(self) -> QuerySet[LimitManager]:
        return LimitManager.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        context["form"] = LimitForm()
        return context
