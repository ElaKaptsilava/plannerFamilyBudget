from celery import shared_task


@shared_task
def update_target_deadlines():
    from django.core.management import call_command

    call_command("update_target_deadlines")
