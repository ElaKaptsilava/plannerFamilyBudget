from budgets_manager.forms import LimitForm
from budgets_manager.models import LimitManager
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


class LimitCreateView(LoginRequiredMixin, CreateView):
    model = LimitManager
    template_name = "budgets_manager/limits/list.html"
    context_object_name = "limit"
    form_class = LimitForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        return context

    def form_valid(self, form):
        plan = form.save(commit=False)
        plan.user = self.request.user
        plan.budget_manager = self.request.user.budgetmanager
        plan.save()
        messages.success(self.request, "The plan added successfully!")
        success_url = reverse_lazy(
            "manager:limits-list", kwargs={"user_id": self.request.user.id}
        )
        return HttpResponseRedirect(success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to add plan. Please check the form.")
        return super().form_invalid(form)
