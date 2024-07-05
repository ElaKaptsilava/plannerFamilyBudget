from django.views.generic import DetailView
from targets.models import Saving


class SavingDetailView(DetailView):
    model = Saving
    template_name = "accounts/dashboard.html"
    context_object_name = "saving"
