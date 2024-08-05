from django.urls import path
from targets.views.contributions.delete_multiple import (
    TargetContributionsDeleteMultipleView,
)
from targets.views.contributions.form_view import TargetContributionsView
from targets.views.savings import NegativeCreateView, PositiveCreateView
from targets.views.targets import (
    TargetDeleteMultipleView,
    TargetsView,
    TargetUpdateView,
)

app_name = "targets"
urlpatterns = [
    path("", TargetsView.as_view(), name="targets-list"),
    path(
        "<int:pk>/update/",
        TargetUpdateView.as_view(),
        name="targets-list-create",
    ),
    path(
        "delete-multiple/",
        TargetDeleteMultipleView.as_view(),
        name="targets-list-delete-multiple",
    ),
    path(
        "<int:pk>/contributions/",
        TargetContributionsView.as_view(),
        name="contributions-list",
    ),
    path(
        "<int:pk>/contributions/create/",
        TargetContributionsView.as_view(),
        name="contributions-list-create",
    ),
    path(
        "<int:pk>/contributions/delete-multiple/",
        TargetContributionsDeleteMultipleView.as_view(),
        name="contributions-list-delete-multiple",
    ),
    path(
        "saving/create/add/",
        PositiveCreateView.as_view(),
        name="saving-contributions-create-positive",
    ),
    path(
        "saving/create/reduce/",
        NegativeCreateView.as_view(),
        name="saving-contributions-create-negative",
    ),
]
