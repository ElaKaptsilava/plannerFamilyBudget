from celery import shared_task


@shared_task
def generate_budget_analysis_message():
    from django.core.management import call_command

    call_command("open_ai_message")
