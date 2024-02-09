# # tasks.py

# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
# from django.core.management import call_command
# # __init__.py in the same app as tasks.py

# from .tasks import scheduler

# __all__ = ("scheduler",)

# scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), "default")

# @scheduler.scheduled_job("interval", minutes=1)
# def my_periodic_task():
#     print("Executing my periodic task...")
#     # You can replace the following command with your actual task logic
#     call_command("my_custom_command")  # Replace with your actual management command

# register_events(scheduler)
