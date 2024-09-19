from django.contrib import messages
from django.shortcuts import redirect


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        """
        Ensure that the object being accessed belongs to the current user.
        """
        obj = self.get_object()
        if obj.user != request.user:
            messages.error(request, "You do not have permission to edit this budget.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
