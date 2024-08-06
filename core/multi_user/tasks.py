import typing

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404
from multi_user.models import Invitation


@shared_task()
def sending_email(params: dict[str, typing.Any]) -> None:
    print("Iam in task")

    invitation_link = params["invitation_link"]
    invitation_id = params["invitation_id"]

    try:
        invitation = Invitation.objects.get(pk=invitation_id)
    except Invitation.DoesNotExist:
        raise Http404("Invitation does not exist")

    subject = "You are invited!"
    message = f"You have been invited. Click the following link to accept the invitation: {invitation_link}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [invitation.email]
    print(recipient_list)
    print(from_email)

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )
