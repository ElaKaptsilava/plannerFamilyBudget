from django.urls import path
from targets.views.targets import target_update, target_formview, target_delete_multiple
from targets.views.contributions import (
    comtributions_form_view,
    contributions_delete_multiple,
)

app_name = "targets"
urlpatterns = [
    path("list/", target_formview.TargetView.as_view(), name="targets-list"),
    path(
        "list/update/<int:pk>/",
        target_update.TargetUpdateView.as_view(),
        name="targets-list-create",
    ),
    path(
        "list/delete-multiple/",
        target_delete_multiple.TargetDeleteMultipleView.as_view(),
        name="targets-list-delete-multiple",
    ),
    path(
        "detail/<int:pk>/contributions/list/",
        comtributions_form_view.TargetContributionsView.as_view(),
        name="contributions-list",
    ),
    path(
        "detail/<int:pk>/contributions/create/",
        comtributions_form_view.TargetContributionsView.as_view(),
        name="contributions-list-create",
    ),
    path(
        "detail/<int:pk>/contributions/delete-multiple/",
        contributions_delete_multiple.TargetContributionsDeleteMultipleView.as_view(),
        name="contributions-list-delete-multiple",
    ),
]
