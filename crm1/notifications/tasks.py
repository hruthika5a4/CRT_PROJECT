# myapp/tasks.py

from celery import shared_task
from plyer import notification

@shared_task
def update_template_task():
    title = 'Template Update Alert'
    message = 'Your template has been altered!'
    notification.notify(
        title=title,
        message=message,
        app_name='TemplateUpdater',
        timeout=10
    )
