from core.celery import app


@app.task(bind=True)
def update_target_deadlines():
    from django.core.management import call_command

    call_command("update_target_deadlines")
