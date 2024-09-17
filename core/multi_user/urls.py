from django.urls import path
from multi_user.views.create import CreateFamilyBudgetView
from multi_user.views.invite_member import InviteMemberView
from multi_user.views.join_to_budget import join_family_budget

app_name = "multiuser"

urlpatterns = [
    path("create/", CreateFamilyBudgetView.as_view(), name="family-budget-list-create"),
    path(
        "invites/<int:family_budget_id>/",
        InviteMemberView.as_view(),
        name="invite-family-member",
    ),
    path("invites/<str:token>/accept/", join_family_budget, name="invite-list-accept"),
]
