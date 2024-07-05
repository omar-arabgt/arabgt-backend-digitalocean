from celery import shared_task

@shared_task
def scheduled_task():
    print("This is a scheduled task")
