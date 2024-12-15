from celery import shared_task

@shared_task(queue='schedule_queue')
def process_schedules(schedule):
    # Process the schedule items one at a time
    pass

@shared_task(queue='default_queue')
def process_asynchronously(task):
    pass