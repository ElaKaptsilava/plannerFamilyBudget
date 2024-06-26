from django.urls import path

from . import views

app_name = "targets"
urlpatterns = [
    path("list/", views.TargetView.as_view(), name="targets-list"),
    path(
        "list/update/<int:pk>/",
        views.TargetUpdateView.as_view(),
        name="targets-list-create",
    ),
    path(
        "list/delete-multiple/",
        views.TargetDeleteMultipleView.as_view(),
        name="targets-list-delete-multiple",
    ),
    path(
        "detail/<int:pk>/contributions/list/",
        views.TargetContributionsView.as_view(),
        name="contributions-list",
    ),
    path(
        "detail/<int:pk>/contributions/create/",
        views.TargetContributionsView.as_view(),
        name="contributions-list-create",
    ),
    path(
        "detail/<int:pk>/contributions/delete-multiple/",
        views.TargetContributionsDeleteMultipleView.as_view(),
        name="contributions-list-delete-multiple",
    ),
]
