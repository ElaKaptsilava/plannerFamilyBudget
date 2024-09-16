from django.urls import path
from multi_user.views.join_to_budget import invite_family_member, join_family_budget

app_name = "multiuser"

urlpatterns = [
    path(
        "invites/<int:family_budget_id>/",
        invite_family_member,
        name="invite-family-member",
    ),
    path("invites/<str:token>/accept/", join_family_budget, name="invite-list-accept"),
]
