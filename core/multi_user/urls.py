from django.urls import path
from multi_user.views.join_to_budget import invite_family_member, join_family_budget

app_name = "multiuser"

urlpatterns = [
    path(
        "invite/<int:family_budget_id>/",
        invite_family_member,
        name="invite-family-member",
    ),
    path("accept_invite/<str:token>/", join_family_budget, name="invite-list-accept"),
]
