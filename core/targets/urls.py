from django.urls import path

from . import views

app_name = "targets"
urlpatterns = [
    path("targets/list/", views.TargetView.as_view(), name="targets-list"),
    path(
        "targets/list/update/<int:pk>/",
        views.TargetUpdateView.as_view(),
        name="targets-list-create",
    ),
    path(
        "list/delete-multiple/",
        views.TargetDeleteMultipleView.as_view(),
        name="targets-list-delete-multiple",
    ),
    path(
        "<int:pk>/contributions/list/",
        views.TargetContributionsView.as_view(),
        name="contributions-list",
    ),
    path(
        "<int:pk>/contributions/create/",
        views.TargetContributionsView.as_view(),
        name="contributions-list-create",
    ),
    path(
        "<int:pk>/contributions/delete-multiple/",
        views.TargetContributionsDeleteMultipleView.as_view(),
        name="contributions-list-delete-multiple",
    ),
]
