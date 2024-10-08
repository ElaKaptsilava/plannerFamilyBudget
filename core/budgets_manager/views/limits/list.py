from budgets_manager.filters import LimitFilterSet
from budgets_manager.forms.limit import LimitForm
from budgets_manager.models import LimitManager
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView


class LimitListView(LoginRequiredMixin, ListView):
    model = LimitManager
    template_name = "budgets_manager/limits/list.html"
    context_object_name = "limits-list"
    filterset_class = LimitFilterSet

    def get_queryset(self) -> QuerySet[LimitManager]:
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        queryset = self.filterset.qs.filter(
            budget_manager=self.request.user.set_budget.budget
        )
        return queryset.select_related("budget_manager")

    def get_context_data(self, **kwargs) -> dict:
        context = {
            "form": LimitForm(),
            "filter": self.filterset,
            "limit_forms": {
                limit.pk: LimitForm(instance=limit) for limit in self.object_list
            }.items(),
        }
        kwargs.update(context)
        if not self.get_queryset().exists():
            messages.info(self.request, "No limits found.")
        return super().get_context_data(**kwargs)
