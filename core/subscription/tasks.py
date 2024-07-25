from celery import shared_task


@shared_task
def update_subscription_status():
    from django.core.management import call_command

    call_command("update_subscription_status")
