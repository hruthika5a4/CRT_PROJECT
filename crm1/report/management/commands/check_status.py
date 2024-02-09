from django.core.management.base import BaseCommand
from django.shortcuts import render
from django.utils import timezone
from report.models import Topic  # Update with your actual model and app name

class Command(BaseCommand):
    help = 'Check the status field in the Topic model every 5 minutes'

    def handle(self, *args, **options):
        # Retrieve topics with 'ns' status and future target_date
        ns_topics = Topic.objects.filter(status='ns', target_date__gt=timezone.now())

        # Render the template with the filtered topics
        context = {'ns_topics': ns_topics, 'timestamp': timezone.now()}
        template_name = 'your_app/check_status_template.html'  # Update with your actual app name
        rendered_template = render(None, template_name, context)

        # Display or log the rendered template (optional)
        self.stdout.write(self.style.SUCCESS(f"Rendered template at {timezone.now()}:\n{check_status_template.html}"))
