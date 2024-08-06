from django.urls import path
from multi_user.views.invitation import AcceptInvitationView, CreateInvitationView

app_name = "multi_user"

urlpatterns = [
    path("invite/send/", CreateInvitationView.as_view(), name="invite-list-create"),
    path(
        "accept_invite/<str:token>/",
        AcceptInvitationView.as_view(),
        name="invite-list-accept",
    ),
]
