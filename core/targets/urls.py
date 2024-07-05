from django.urls import path
from targets.views.contributions.delete_multiple import (
    TargetContributionsDeleteMultipleView,
)
from targets.views.contributions.form_view import TargetContributionsView
from targets.views.savings import SavingContributionCreateView
from targets.views.targets import (
    TargetDeleteMultipleView,
    TargetsView,
    TargetUpdateView,
)

app_name = "targets"
urlpatterns = [
    path("list/", TargetsView.as_view(), name="targets-list"),
    path(
        "list/update/<int:pk>/",
        TargetUpdateView.as_view(),
        name="targets-list-create",
    ),
    path(
        "list/delete-multiple/",
        TargetDeleteMultipleView.as_view(),
        name="targets-list-delete-multiple",
    ),
    path(
        "detail/<int:pk>/contributions/list/",
        TargetContributionsView.as_view(),
        name="contributions-list",
    ),
    path(
        "detail/<int:pk>/contributions/create/",
        TargetContributionsView.as_view(),
        name="contributions-list-create",
    ),
    path(
        "detail/<int:pk>/contributions/delete-multiple/",
        TargetContributionsDeleteMultipleView.as_view(),
        name="contributions-list-delete-multiple",
    ),
    path(
        "saving/create/",
        SavingContributionCreateView.as_view(),
        name="saving-contributions-create",
    ),
]
